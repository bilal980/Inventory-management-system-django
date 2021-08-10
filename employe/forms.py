from employe.models import Employee, EmployeeSalary
from django import forms


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'father_name', 'cnic',
                  'mobile', 'address', 'date_of_joining']
        labels = {'date_of_joining': 'Enter Date'}
        widgets = {'name': forms.TextInput(attrs={'type': "text", 'placeholder': "Name", 'class': 'form-control name', 'name': "employe_name"}), 
        'father_name': forms.TextInput(
            attrs={'type': "text", 'placeholder': "Father Name (Optional)", 'class': 'form-control father_name', 'name': "father_name", }), 'address': forms.Textarea(
            attrs={'rows': "2", 'placeholder': "Address (Optional)", 'class': 'form-control adress', 'name': "adress", }), 'shop': forms.TextInput(
            attrs={'type': "text", 'placeholder': "Shop Name", 'class': 'form-control shop', 'name': "shop", }),
            'cnic': forms.TextInput(
            attrs={'type': "text", 'placeholder': "CNIC", 'class': 'form-control cnic', 'name': "CNIC", }), 
            'mobile': forms.TextInput(
            attrs={'type': "text", 'placeholder': "Mobile", 'class': 'form-control shop', 'name': "mobile", }), }



class EmployeeSalaryForm(forms.ModelForm):
    class Meta:
        model = EmployeeSalary
        fields = '__all__'
