from django.db import models
from django.utils import timezone

# Create your models here.
class Employee(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    father_name = models.CharField(max_length=100, null=True, blank=True)
    cnic = models.CharField(max_length=100, null=True, blank=True)
    mobile = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    date_of_joining = models.DateField(default=timezone.now)

    def __str__(self):
        return self.name

class EmployeeSalary(models.Model):
    employee = models.ForeignKey(Employee, related_name='employee_salary',
                                 null=True, blank=True, on_delete=models.CASCADE)
    salary_amount = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateField(null=True, blank=True)
   
