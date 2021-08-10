from django.urls import path
from customer import views
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('', login_required(views.CustomerListView.as_view(),login_url='/'), name='customer'),
    path('add_customer/', login_required(views.CustomerCreateView.as_view(),login_url='/'), name='add_customer'),
    path('update_customer/<int:pk>', login_required(views.CustomerUpdateView.as_view(),login_url='/'), name='update_customer'),
    path('delete/<int:pk>', login_required(views.CustomerDeleteView.as_view(),login_url='/'), name='delete_customer'),
]
