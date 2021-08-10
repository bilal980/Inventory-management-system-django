from django.urls import path
from django.contrib.auth.decorators import login_required
from purchase.views import PurchaseListView,PurchaseSingleListView
from product.views import StockInListView
urlpatterns = [
    path('', login_required(PurchaseListView.as_view(),login_url='/'), name='purchase'),
    path('detail_purchase/<int:pk>', login_required(PurchaseSingleListView.as_view(),login_url='/'), name='purchasesingle'),
    
]
