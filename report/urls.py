from django.urls import path
from report import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
        path('', login_required(views.DailyStockLogs.as_view(),login_url='/'),name='daily_stock_logs'),
        path('monthly/', login_required(views.MonthlyStockLogs.as_view(),login_url='/'),name='monthly_stock_logs'),

]
