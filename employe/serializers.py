from rest_framework import serializers
# Create your serializers here.


class EmployeeSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100, null=True, blank=True)
    father_name = serializers.CharField(max_length=100, null=True, blank=True)
    cnic = serializers.CharField(max_length=100, null=True, blank=True)
    mobile = serializers.CharField(max_length=100, null=True, blank=True)
    address = serializers.CharField(max_length=100, null=True, blank=True)
    date_of_joining = serializers.DateField(default=timezone.now)

  

class EmployeeSalary(serializers.Model):
    employee = serializers.ForeignKey(Employee, related_name='employee_salary',
                                 null=True, blank=True, on_delete=serializers.CASCADE)
    salary_amount = serializers.CharField(max_length=100, null=True, blank=True)
    date = serializers.DateField(null=True, blank=True)
