from django.shortcuts import redirect, HttpResponseRedirect, reverse
from django.contrib import messages
from django.db import transaction
from product.models import Product, StockIn, StockOut
from django.views.generic import ListView, DetailView, FormView, TemplateView
from django.core.cache import cache
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from product.forms import StockOutForm, StockDetailsForm, ProductForm, StockDetailsForm
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


class ProductCreateView(FormView):
    form_class = StockDetailsForm
    template_name = "add_product.html"

    def post(self, request, *args, **kwargs):
        try:
            product_name = request.POST.get('name', 'None')
            brand_name = request.POST.get('brand_name', 'None')
            unit_type = request.POST.get('unit_type', 'None')
            if unit_type=='None':
                unit_type='Quantity'
            bar_code = request.POST.get('bar_code', 'None')
            quantity = request.POST.get('quantity', 'None')
            buying_price_item = request.POST.get('buying_price_item', 'None')
            price_per_item = request.POST.get('price_per_item', 'None')
            dated_order = request.POST.get('dated_order', 'None')
            total_amount = request.POST.get('total_amount', 'None')
            total_buying_amount = request.POST.get('total_buying_amount', 'None')
            stock_expiry = request.POST.get('stock_expiry', 'None')

            with transaction.atomic():
                prod_form_kwargs = {
                    'unit_type': unit_type,
                    'name': product_name,
                    'brand_name': brand_name,
                    'bar_code': bar_code
                }

                product_form = ProductForm(prod_form_kwargs)
                if product_form.is_valid():
                    print('prodouct form successfully Created')
                    product = product_form.save()

                stockIn_kwargs = {
                    'product': product,
                    'quantity': quantity,
                    'price_per_item': price_per_item,
                    'total_amount': total_amount,
                    'buying_price_item': buying_price_item,
                    'total_buying_amount': total_buying_amount,
                    'dated_order': dated_order,
                    'stock_expiry': stock_expiry
                }
                stockinform = StockDetailsForm(stockIn_kwargs)
                if stockinform.is_valid():
                    stockinform.save()
                messages.success(request,"Product Added!")
                return redirect(reverse_lazy('product'))
        except:
            messages.warning(request,'Product Not Added!')
            return redirect(reverse_lazy('product'))

class ProductUpdateView(UpdateView):
    template_name = 'update_product.html'
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('product')

    def form_valid(self, form):
        messages.success(self.request, 'Product Updated Successfully!')
        return super().form_valid(form)

class ProductItemList(ListView):
    template_name = 'product.html'
    context_object_name = 'products'
    model = Product
    paginate_by = 40
    ordering = '-id'

    def dispatch(self, request, *args, **kwargs):
        return super(ProductItemList, self).dispatch(request, *args, **kwargs)

class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            cache.clear()
            return HttpResponseRedirect(reverse_lazy('login'))
        return super(ProductDetailView, self).dispatch(request, *args, **kwargs)

class StockOutItems(FormView):
    form_class = StockOutForm
    template_name = 'add_stock_out.html'

    def dispatch(self, request, *args, **kwargs):
        return super(StockOutItems, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        product_item_detail = form.save()
        messages.success(self.request, message='Stock Out Successfully!')
        return HttpResponseRedirect(reverse_lazy('stock_out_list', args=[
            self.kwargs.get('product_id')])
        )

    def form_invalid(self, form):
        return super(StockOutItems, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(StockOutItems, self).get_context_data(**kwargs)
        try:
            product = (Product.objects.get(id=self.kwargs.get('product_id'))
                       )
        except ObjectDoesNotExist:
            raise Http404('Product not found with concerned User')

        context.update({
            'product': product
        })
        return context

class AddStockItems(CreateView):
    template_name = 'add_stock_in.html'
    form_class = StockDetailsForm
    success_url = '/product/'

    def dispatch(self, request, *args, **kwargs):
   
        return super(AddStockItems, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        product_item_detail = form.save()
        messages.success(self.request, 'Stock In Successfully!')
        return HttpResponseRedirect(reverse('stock_in_list', args=[self.kwargs.get('pk')]))

    def form_invalid(self, form):
        return super(AddStockItems, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(AddStockItems, self).get_context_data(**kwargs)
        try:
            product = (Product.objects.get(id=self.kwargs.get('pk'))
                       )
        except ObjectDoesNotExist:
            raise Http404('Product not found with concerned User')

        context.update({
            'product': product
        })
        return context

class StockInListView(ListView):
    template_name = 'stock_in_list.html'
    paginate_by = 30
    model = StockIn
    ordering = '-id'

    def get_queryset(self):
        queryset = self.queryset
        if not queryset:
            queryset = StockIn.objects.all()

        queryset = queryset.filter(product=self.kwargs.get('pk'))
        return queryset.order_by('-id')

    def get_context_data(self, **kwargs):
        context = super(StockInListView, self).get_context_data(**kwargs)
        context.update({
            'product': Product.objects.get(id=self.kwargs.get('pk'))
        })
        return context

class StockOutDeleteView(DeleteView):
    model = StockOut
    template_name = "stock_in_list.html"

    def get(self, request, *args, **kwargs):
        self.success_url = request.META.get('HTTP_REFERER', '/product/')
        messages.warning(self.request,'StockOut Record Deleted!')
        return self.delete(request, *args, **kwargs)

class StockInDeleteView(DeleteView):
    model = StockIn
    template_name = "stock_in_list.html"

    def get(self, request, *args, **kwargs):
        self.success_url = request.META.get('HTTP_REFERER', '/product/')
        messages.warning(self.request,'StockIn Record Deleted!')
        return self.delete(request, *args, **kwargs)

class StockOutListView(ListView):
    template_name = 'stock_out_list.html'
    paginate_by = 30
    model = StockOut
    ordering = '-id'

    def get_queryset(self, **kwargs):
        queryset = self.queryset
        if not queryset:
            queryset = StockOut.objects.all()

        queryset = queryset.filter(product=self.kwargs.get('pk'))
        return queryset.order_by('-id')

    def get_context_data(self, **kwargs):
        context = super(StockOutListView, self).get_context_data(**kwargs)
        context.update({
            'product': Product.objects.get(id=self.kwargs.get('pk'))
        })
        return context

class StockInUpdateView(UpdateView):
    template_name = 'stock_in_update.html'
    model = StockIn
    form_class = StockDetailsForm
    success_url = '/product/'

    def form_valid(self, form):
        messages.success(self.request, 'StockIn Updated Successfully!')
        return super().form_valid(form)

class ProductDeleteView(DeleteView):
    model = Product
    template_name = "product.html"
    success_url = '/product/'

    def get(self, request, *args, **kwargs):
        messages.warning(request,'Product Deleted!')
        return self.delete(request, *args, **kwargs)
