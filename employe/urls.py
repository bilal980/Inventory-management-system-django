from django.urls import path
from employe import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', login_required(views.EmployeeListView.as_view(),login_url='/'), name='employe'),
    path('add_employe/', login_required(views.EmployeCreateView.as_view(),login_url='/'), name='add_employe'),
    path('update/employe/<int:pk>', login_required(views.EmployeeUpdateView.as_view(),login_url='/'), name='update_employe'),
    path('delete_employe/<int:pk>', login_required(views.EmployeeDeleteView.as_view(),login_url='/'), name='delete_employe'),
    path('salary_employe/<int:pk>', login_required(views.EmployeeSalaryCreateView.as_view(),login_url='/'), name='add_salary'),
    path('detail_salary/<int:pk>', login_required(views.EmployeeSalaryDetailView.as_view(),login_url='/'), name='detail_salary'),
    path('delete/salary/<int:pk>', login_required(views.EmployeeSalaryDeleteView.as_view(),login_url='/'), name='delete_salary'),
]
