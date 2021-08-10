from django.urls import path
from expense import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('',login_required(views.ExtraExpenseListView.as_view(),login_url='/'),name='expense_list'),
    path('add_expense/', login_required(views.ExtraExpenseCreateView.as_view(),login_url='/'), name='add_expense'),
    path('delete_expense/<int:pk>', login_required(views.ExtraExpenseDeleteView.as_view(),login_url='/'), name='delete_expense'),
]
