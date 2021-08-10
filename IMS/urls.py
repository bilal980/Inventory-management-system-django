from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.decorators import login_required
from .views import login_, logout_
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',login_, name='login'),
    path('logout/', login_required(logout_, login_url='/'), name='logout'),
    path('dashboard/', include('dashboard.urls')),
    path('customer/', include('customer.urls')),
    path('employe/', include('employe.urls')),
    path('expense/', include('expense.urls')),
    path('product/', include('product.urls')),
    path('purchase/', include('purchase.urls')),
    path('report/', include('report.urls')),
    path('sale/', include('sale.urls')),
    path('setting/', include('setting.urls')),
    path('supplier/', include('supplier.urls')),
    path('ledger/', include('ledger.urls')),


    # theme api
    # path('name/', Business_Name, 'business_name'),
    # path('theme/',views_api.theme,name='theme'),
]
