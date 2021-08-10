from django.shortcuts import HttpResponse
from django.http import JsonResponse
import json
from ledger.forms import LedgerForm
from customer.forms import CustomerForm
from django.contrib import messages
from django.db import transaction
from sale.models import SalesHistory
from django.urls import reverse_lazy
from customer.models import Customer
from product.models import Product, ProductDetail, StockIn, PurchasedProduct, StockOut, ExtraItems
from ledger.models import Ledger
from django.utils import timezone
from django.views.generic import View, ListView, FormView, TemplateView, DeleteView
from sale.forms import SaleForm
from django.views.decorators.csrf import csrf_exempt
from product.forms import PurchasedProductForm, StockOutForm, ExtraItemsForm


class Invoice(FormView):
    form_class = SaleForm
    template_name = 'add_sale.html'
    success_url = '/sale_history/'

    def get_context_data(self, **kwargs):
        context = super(Invoice, self).get_context_data(**kwargs)
        products = (
            StockIn.objects.all()
        )
        customers = (
            Customer.objects.all()
        )
        context.update({
            'products': products,
            'customers': customers,
            'present_date': timezone.now().date(),
        })
        return context


class UpdateInvoice(FormView):
    form_class = SaleForm
    template_name = 'update_invoice.html'

    def get_context_data(self, **kwargs):
        context = super(UpdateInvoice, self).get_context_data(**kwargs)
        products = (
            StockIn.objects.all()
        )
        customers = (
            Customer.objects.all()
        )
        invoice = SalesHistory.objects.get(id=self.kwargs.get('pk'))
        invoice_customer=invoice.customer
        context.update({
            'invoice_customer':invoice_customer,
            'products': products,
            'customers': customers,
            'present_date': timezone.now().date(),
            'invoice': invoice
        })
        return context


class GenerateInvoiceAPIView(View):

    def __init__(self, *args, **kwargs):
        super(GenerateInvoiceAPIView, self).__init__(*args, **kwargs)
        self.customer = None
        self.invoice = None

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(GenerateInvoiceAPIView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        subtotal = request.POST.get('subtotal')
        discount = request.POST.get('discount')
        shipping = request.POST.get('shipping')
        gr_total = request.POST.get('gr_total')
        totalQty = request.POST.get('totalQty')
        
        rm_amount = request.POST.get('rm_amount')
        paid_amount = request.POST.get('paid_amount')
        cash_payment = request.POST.get('cash_payment')
        rt_cash = request.POST.get('rt_cash')
        items = json.loads(request.POST.get('items'))

        purchased_items_id = []
        extra_items_id = []
        try:
            with transaction.atomic():
                sale_form_kwargs = {
                    'discount': discount,
                    'grand_total': gr_total,
                    'total_quantity': totalQty,
                    'shipping': shipping,
                    'paid_amount': paid_amount,
                    'remaining_payment': rm_amount,
                    'cash_payment': cash_payment,
                    'returned_payment': rt_cash,
                }

                if self.request.POST.get('customerid'):
                    print('Running')
                    sale_form_kwargs.update({
                        'customer': self.request.POST.get('customerid')
                    })
                else:
                    customer_form_kwargs = {
                        'customer_name': request.POST.get('customer_name'),
                        'customer_phone': request.POST.get('customer_phone'),
                    }
                    customer_form = CustomerForm(customer_form_kwargs)
                    if customer_form.is_valid():
                        self.customer = customer_form.save()
                        sale_form_kwargs.update({
                            'customer': self.customer.id
                        })

                sale_form = SaleForm(sale_form_kwargs)
                if sale_form.is_valid():
                    self.invoice = sale_form.save()
                
                receipt_number=f'00{self.invoice.id}'
                
                for item in items:
                    # bug
                    try:
                        item_id = item.get('item_id')
                        prod_name = item.get('item_name')
                        product = Product.objects.get(id=item_id)
                        form_kwargs = {
                            'product': product.id,
                            'invoice': self.invoice.id,
                            'quantity': item.get('qty'),
                            'price': item.get('price'),
                            'purchase_amount': item.get('total'),
                        }
                        form = PurchasedProductForm(form_kwargs)
                        if form.is_valid():
                            purchased_item = form.save()
                            purchased_items_id.append(purchased_item.id)

                            latest_stock_in = (
                                StockIn.objects.filter(
                                    product=product.id).latest('id')
                                # StockIn.objects.filter(id=product.id).latest('id')
                            )
                            stock_out_form_kwargs = {
                                'product': product.id,
                                'invoice': self.invoice.id,
                                'purchased_item': purchased_item.id,
                                'stock_out_quantity': float(item.get('qty')),
                                'buying_price': (
                                    float(latest_stock_in.buying_price_item) *
                                    float(item.get('qty'))),
                                'selling_price': (
                                    float(item.get('price')) * float(item.get('qty'))),
                                'dated': timezone.now().date()
                            }

                            stock_out_form = StockOutForm(
                                stock_out_form_kwargs)
                            if stock_out_form.is_valid():
                                stock_out = stock_out_form.save()
                    except:
                        try:
                            extra_item_kwargs = {
                                'item_name': item.get('item_name'),
                                'quantity': item.get('qty'),
                                'price': item.get('price'),
                                'total': item.get('total'),
                                'invoice': self.invoice.id,
                            }
                            extra_item_form = ExtraItemsForm(extra_item_kwargs)
                            if extra_item_form.is_valid():
                                extra_item = extra_item_form.save()
                                extra_items_id.append(extra_item.id)
                        except:
                            raise KeyError

                self.invoice.purchased_items.set(purchased_items_id)
                self.invoice.extra_items.set(extra_items_id)
                self.invoice.receipt_no=f'00{self.invoice.id}'
                self.invoice.save()

                if self.customer or self.request.POST.get('customerid'):
                    if float(rm_amount):
                        ledger_form_kwargs = {
                            'customer': (
                                self.request.POST.get('customerid') or
                                self.customer.id),
                            'invoice': self.invoice.id,
                            'amount': rm_amount,
                            # 'payment':paid_amount,
                            'description': (
                                'Remaining Payment for Bill/Receipt No %s '
                                % self.invoice.receipt_no),
                            'dated': timezone.now()
                        }

                        ledgerform = LedgerForm(ledger_form_kwargs)
                        if ledgerform.is_valid():
                            ledger = ledgerform.save()
                messages.success(request, 'Invoice created Successfully!')
                return JsonResponse({'invoice_id': self.invoice.id})
        except:
            messages.error(request, 'Please Fill Form Correctly')
            return JsonResponse({'Error': 'Error'})


class UpdateInvoiceView(View):

    def __init__(self, *args, **kwargs):
        super(UpdateInvoiceView, self).__init__(*args, **kwargs)
        self.customer = None
        self.invoice = None

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(UpdateInvoiceView, self).dispatch(request, *args, **kwargs)
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        subtotal = request.POST.get('subtotal')
        discount = request.POST.get('discount')
        shipping = request.POST.get('shipping')
        gr_total = request.POST.get('gr_total')
        totalQty = request.POST.get('totalQty')
        rm_amount = request.POST.get('rm_amount')
        paid_amount = request.POST.get('paid_amount')
        cash_payment = request.POST.get('cash_payment')
        rt_cash = request.POST.get('rt_cash')
        items = json.loads(request.POST.get('items'))
        purchased_items_id = []
        extra_items_id = []
        try:
            with transaction.atomic():
                receipt_no=SalesHistory.objects.get(id=request.POST.get('invoice_id')).receipt_no
                SalesHistory.objects.get(id=request.POST.get('invoice_id')).delete()
                sale_form_kwargs = {    
                    'receipt_no': receipt_no,
                    'discount': discount,
                    'grand_total': gr_total,
                    'total_quantity': totalQty,
                    'shipping': shipping,
                    'paid_amount': paid_amount,
                    'remaining_payment': rm_amount,
                    'cash_payment': cash_payment,
                    'returned_payment': rt_cash,
                }

                if self.request.POST.get('customerid'):
                    sale_form_kwargs.update({
                        'customer': self.request.POST.get('customerid')
                    })
                else:
                    customer_form_kwargs = {
                        'customer_name': request.POST.get('customer_name'),
                        'customer_phone': request.POST.get('customer_phone'),
                    }
                    customer_form = CustomerForm(customer_form_kwargs)
                    if customer_form.is_valid():
                        self.customer = customer_form.save()
                        sale_form_kwargs.update({
                            'customer': self.customer.id
                        })

                sale_form = SaleForm(sale_form_kwargs)
                self.invoice = sale_form.save()
                for item in items:
                    # bug
                    try:
                        item_id = item.get('item_id')
                        product = Product.objects.get(id=item_id)
                        form_kwargs = {
                            'product': product.id,
                            'invoice': self.invoice.id,
                            'quantity': item.get('qty'),
                            'price': item.get('price'),
                            'purchase_amount': item.get('total'),
                        }
                        form = PurchasedProductForm(form_kwargs)
                        if form.is_valid():
                            purchased_item = form.save()
                            purchased_items_id.append(purchased_item.id)

                            latest_stock_in = (
                                StockIn.objects.filter(
                                    product=product.id).latest('id')
                                # StockIn.objects.filter(id=product.id).latest('id')
                            )
                            stock_out_form_kwargs = {
                                'product': product.id,
                                'invoice': self.invoice.id,
                                'purchased_item': purchased_item.id,
                                'stock_out_quantity': float(item.get('qty')),
                                'buying_price': (
                                    float(latest_stock_in.buying_price_item) *
                                    float(item.get('qty'))),
                                'selling_price': (
                                    float(item.get('price')) * float(item.get('qty'))),
                                'dated': timezone.now().date()
                            }

                            stock_out_form = StockOutForm(
                                stock_out_form_kwargs)
                            if stock_out_form.is_valid():
                                stock_out = stock_out_form.save()
                    except:
                        try:
                            extra_item_kwargs = {
                                'item_name': item.get('item_name'),
                                'quantity': item.get('qty'),
                                'price': item.get('price'),
                                'total': item.get('total'),
                                'invoice': self.invoice.id,
                            }
                            extra_item_form = ExtraItemsForm(extra_item_kwargs)
                            if extra_item_form.is_valid():
                                extra_item = extra_item_form.save()
                                extra_items_id.append(extra_item.id)
                        except:
                            raise KeyError

                self.invoice.purchased_items.set(purchased_items_id)
                self.invoice.extra_items.set(extra_items_id)
                self.invoice.save()

                if self.customer or self.request.POST.get('customerid'):
                    if float(rm_amount):
                        ledger_form_kwargs = {
                            'customer': (
                                self.request.POST.get('customerid') or
                                self.customer.id),
                            'invoice': self.invoice.id,
                            'amount': rm_amount,
                            'description': (
                                'Remaining Payment for Bill/Receipt No %s '
                                % self.invoice.receipt_no),
                            'dated': timezone.now()
                        }

                        ledgerform = LedgerForm(ledger_form_kwargs)
                        if ledgerform.is_valid():
                            ledger = ledgerform.save()
                            print('Ending....')
                messages.success(request, 'Invoice Updated!')
                return JsonResponse({'invoice_id': self.invoice.id})
        except:
            messages.error(request, 'Please Fill Form Correctly')
            return JsonResponse({'Error': 'Error'})


class InvoicesList(ListView):
    template_name = 'invoice_list.html'
    model = SalesHistory
    paginate_by = 30
    ordering = ('-id',)

    def dispatch(self, request, *args, **kwargs):
        return super(InvoicesList, self).dispatch(request, *args, **kwargs)


class InvoiceDetailView(TemplateView):
    template_name = 'invoice_detail.html'

    def dispatch(self, request, *args, **kwargs):

        return super(
            InvoiceDetailView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(InvoiceDetailView, self).get_context_data(**kwargs)
        invoice = SalesHistory.objects.get(id=self.kwargs.get('pk'))
        context.update({
            'invoice': invoice,
            'product_details': invoice.product_details,
            'extra_items_details': invoice.extra_items
        })
        return context


class SalesDeleteView(DeleteView):
    model = SalesHistory
    success_url = reverse_lazy('sale')

    def get(self, request, *args, **kwargs):
        PurchasedProduct.objects.filter(
            invoice__id=self.kwargs.get('pk')).delete()
        StockOut.objects.filter(
            invoice__id=self.kwargs.get('pk')).delete()
        Ledger.objects.filter(
            invoice__id=self.kwargs.get('pk')).delete()
        messages.warning(self.request, 'Invoice Deleted Successfully!')
        return self.delete(request, *args, **kwargs)


# for fetching stock available and quantity
@csrf_exempt
def available(request):
    if request.method == 'POST':
        try:
            stock_availabe = Product.objects.get(id=request.POST.get('item_name'))
            try:
                st_available = int(stock_availabe.product_available_items())
            except:
                st_available = int(0)
            try:
                selling_price = StockIn.objects.filter(
                    product=stock_availabe).last()
                sel_price = int(selling_price.price_per_item)
            except:
                sel_price = int(0)
            json_data = {"stock_available": st_available,
                         "selling_price": sel_price}
            return JsonResponse(json.dumps(json_data), safe=False)
        except:
            return HttpResponse(None)