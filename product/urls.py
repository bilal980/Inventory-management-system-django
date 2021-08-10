from django.urls import path
from product import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
 path('',login_required(views.ProductItemList.as_view(),login_url='/'),name='product'), 
 path('add_product/', login_required(views.ProductCreateView.as_view(),login_url='/'), name='add_product'),
 path('product_details/<int:pk>', login_required(views.ProductDetailView.as_view(),login_url='/'), name='product_detail'),
 path('product_update/<int:pk>', login_required(views.ProductUpdateView.as_view(),login_url='/'), name='product_update'),
 path('product_delete/<int:pk>', login_required(views.ProductDeleteView.as_view(),login_url='/'), name='product_delete'),
 path('add_stock_out/<int:product_id>', login_required(views.StockOutItems.as_view(),login_url='/'), name='add_stock_out'),
 path('add_stock_in/<int:pk>', login_required(views.AddStockItems.as_view(),login_url='/'), name='add_stock_in'),
 path('stock_in_list/<int:pk>', login_required(views.StockInListView.as_view(),login_url='/'), name='stock_in_list'),
 path('stockin/delete/<int:pk>', login_required(views.StockInDeleteView.as_view(),login_url='/'), name='stockin_delete'),
 path('stockout/delete/<int:pk>', login_required(views.StockOutDeleteView.as_view(),login_url='/'), name='stockout_delete'),
 path('stock_out_list/<int:pk>', login_required(views.StockOutListView.as_view(),login_url='/'), name='stock_out_list'),
 path('stock_in_update/<int:pk>', login_required(views.StockInUpdateView.as_view(),login_url='/'), name='stock_in_update'),
]
