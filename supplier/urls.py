from django.urls import path
from supplier import views
from django.contrib.auth.decorators import login_required
urlpatterns = [
    path('', login_required(views.SupplierListView.as_view(),login_url='/'), name='supplier'),
    path('add_supplier/', login_required(views.SupplierCreateView.as_view(),login_url='/'), name='add_supplier'),
    path('statement_list/<int:pk>', login_required(views.SupplierStatementListView.as_view(),login_url='/'), name='list_supplier_statement'),
    path('supplier/delete/<int:pk>', login_required(views.SupplierDeleteView.as_view(),login_url='/'), name='delete_supplier'),
    path('add_statement/<int:pk>',login_required(views.AddSupplierStatementCreateView.as_view(),login_url='/'), name='add_supplier_statement'),
    path('add_statement_payment/<int:pk>',login_required(views.StatementPaymentCreateView.as_view(),login_url='/'), name='add_statement_payment'),
    path('update_statement/<int:pk>', login_required(views.SupplierStatementUpdateView.as_view(),login_url='/'), name='update_statement'),
    path('delete/statement/<int:pk>', login_required(views.SupplierStatementDeleteView.as_view(),login_url='/'), name='delete_statement'),
]
