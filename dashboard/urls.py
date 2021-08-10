from django.urls import path
from dashboard import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', login_required(views.DashboardView.as_view(), login_url='/'), name='dashboard'),
    path('staff/', login_required(views.Staff.as_view(), login_url='/'), name='staff'),
    path('stockIn/', login_required(views.all_stock_in, login_url='/'), name='all_stock_in'),
    path('context/', views.dashboard_context, name='dashboard_context'),
]