from django.shortcuts import render
from django.utils.dateformat import DateFormat
from customer.models import Customer
from django.db.models import Sum
from sale.models import SalesHistory
from supplier.models import Supplier
from django.views.generic import TemplateView
from product.models import Product, StockIn, StockOut, PurchasedProduct
from expense.models import ExtraExpense
from django.core.paginator import Paginator
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import Http404
# Create your views here.
class DashboardView(TemplateView):
    template_name = "dashboard.html"

class Staff(TemplateView):
    template_name = "staff.html"

def all_stock_in(request):
    recently_added = StockIn.objects.all().order_by('-id')
    paginator = Paginator(recently_added, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'stock_in.html', {'recently_added': page_obj})

@api_view(['GET'])
def dashboard_context(request):
    context = {}
    all_product = Product.objects.all()
    # serializer = ProductSerializer(all_product, many=True)
    # return Response(serializer.data)
    available_item = {}
    available_item_context = {}
    for product in all_product:
        try:
            item = StockIn.objects.filter(product=product)
            item_name = product.name
            brand_name = product.brand_name
            obj_stockin_quantity = item.aggregate(Sum('quantity'))
            stockin_quantity = float(obj_stockin_quantity.get('quantity__sum'))
        except:
            stockin_quantity = 0

        # stockout
        try:
            item = StockOut.objects.filter(product=product)
            item_name = product.name
            obj_stockout_quantity = item.aggregate(Sum('stock_out_quantity'))
            stockout_quantity = float(
                obj_stockout_quantity.get('stock_out_quantity__sum'))
        except:
            stockout_quantity = 0

        available = stockin_quantity-stockout_quantity
        available_item.update(
            {available: {'item_name': item_name, 'brand_name': brand_name}})

    for i, k in sorted(available_item.items()):

        available_item_context.update({i: k})

    recently_added = StockIn.objects.all().order_by('-id')[:7]
    recently_added_list = []
    for i in recently_added:
        recently_added_list.append({
            'item_name': i.product.name,
            'sale_price': i.price_per_item
        })

    # Total sales amount
    try:
        sales = SalesHistory.objects.aggregate(Sum('grand_total'))
        total_sales = float(sales.get('grand_total__sum'))
    except:
        total_sales = 0
    # total sale dues
    try:
        sales_due = PurchasedProduct.objects.aggregate(Sum('purchase_amount'))
        total_sales_due = float(sales_due.get('purchase_amount__sum'))
    except:
        total_sales_due = 0

    try:
        expenses = ExtraExpense.objects.aggregate(Sum('amount'))
        total_expense = float(expenses.get('amount__sum'))
    except:
        total_expense = 0

    try:
        purchase_amount = StockIn.objects.aggregate(Sum('total_buying_amount'))
        total_purchase_amount = float(purchase_amount.get('total_buying_amount__sum'))
    except:
        total_purchase_amount=0

    recently_sales_list = []
    try:
        recently_sales = SalesHistory.objects.all().order_by('-id')[:6]
        for i in recently_sales:
            df=DateFormat(i.created_at)
            date = df.format('y-m-d')
            cus='unknown'
            if i.customer:
                cus=i.customer.customer_name
            recently_sales_list.append({'customer_name':cus,'quantity':i.total_quantity,'grand_total':i.grand_total,'date': date
            })            
    except:
        raise Http404
    customer = Customer.objects.all().count()
    supplier = Supplier.objects.all().count()
    sale_invoice = SalesHistory.objects.all().count()
    purchase_invoice = StockIn.objects.all().count()

    context.update({'recently_sales_list': recently_sales_list, 'purchase_invoice': purchase_invoice, 'sale_invoice': sale_invoice, 'supplier': supplier, 'customer': customer, 'total_sales_due': total_sales_due, 'total_sale_amount': total_sales, 'total_sales': total_sales, 'available_item_context': available_item_context,
                    'recently_added': recently_added_list, 'total_purchase_amount': total_purchase_amount, 'total_expense': total_expense})
    return Response(context)
