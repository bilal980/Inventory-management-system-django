from django.urls import path
from sale import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', login_required(views.InvoicesList.as_view(),login_url='/'), name='sale'),
    path('add_sale_form/', login_required(views.Invoice.as_view(),login_url='/'), name='add_sale_form'),
    path('add_sale/', login_required(views.GenerateInvoiceAPIView.as_view(),login_url='/'), name='add_sale'),
    path('update_invoice/<int:pk>', login_required(views.UpdateInvoice.as_view(), login_url='/'), name='invoice_update'),
    path('update/invoice/', login_required(views.UpdateInvoiceView.as_view(),login_url='/'), name='update_invoice'),
    path('detail_invoice/<int:pk>', login_required(views.InvoiceDetailView.as_view(),login_url='/'), name='invoice_detail'),
    path('delete_invoice/<int:pk>', login_required(views.SalesDeleteView.as_view(),login_url='/'), name='delete'),
    path('stock_available/', views.available, name='available'),

]
