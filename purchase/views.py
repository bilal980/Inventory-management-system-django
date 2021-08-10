from django.views.generic import ListView
from product.models import Product, StockIn
# Create your views here.


class PurchaseListView(ListView):
    model = Product
    template_name = "purchase_list.html"
    paginate_by=40
    ordering='name'

    
class PurchaseSingleListView(ListView):
    template_name = 'single_item_list.html'
    paginate_by = 40
    model = StockIn
    ordering = '-id'

    def get_queryset(self):
        queryset = self.queryset
        if not queryset:
            queryset = StockIn.objects.all()

        queryset = queryset.filter(product=self.kwargs.get('pk'))
        return queryset.order_by('-id')

    def get_context_data(self, **kwargs):
        context = super(PurchaseSingleListView, self).get_context_data(**kwargs)
        context.update({
            'product': Product.objects.get(id=self.kwargs.get('pk'))
        })
        return context
