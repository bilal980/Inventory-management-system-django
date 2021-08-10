from django.urls import path
from ledger import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('add_new/ledger', login_required(views.AddNewLedger.as_view(),login_url='/'), name='add_new_ledger'),
    path('list_ledger/', views.customer_ledger_view,name='customer_ledger_list'),
    path('customer_ledger_detail/<int:pk>',login_required(views.customer_ledger_detail_list,login_url='/'),name='customer_ledger_detail'),
    path('add/customer_ledger/<int:pk>',login_required(views.AddLedger.as_view(),login_url='/'),name='add_ledger'),
    path('delete/<int:pk>',login_required(views.LedgerDeleteView.as_view(),login_url='/'),name='delete_ledger'),
    path('customer/delete/<int:pk>',login_required(views.CustomerLedgerDeleteView.as_view(),login_url='/'),name='delete_customer_ledger'),
    path('add_payment/<int:pk>',login_required(views.AddPayment.as_view(),login_url='/'),name='add_payment'),

]
