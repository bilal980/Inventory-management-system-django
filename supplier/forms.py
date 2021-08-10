from django import forms
from supplier.models import Supplier, SupplierStatement


class AddSupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'phone', 'CNIC']
        labels = {'name': "Enter Name",
                  'phone': "Enter Mobile", 'CNIC': 'Enter Cnic'}
        # widgets = {'name': forms.TextInput(attrs={'type': "text", 'placeholder': "Supplier Name", 'class': 'form-control name', 'name': "name"}), 'phone': forms.TextInput(
        #     attrs={'type': "text", 'placeholder': "Supplier Phone", 'class': 'form-control phone', 'name': "phone", }), 'CNIC': forms.TextInput(
        #     attrs={'type': "text", 'placeholder': "CNIC", 'class': 'form-control cnic', 'name': "cnic", }), }


class SupplierStatementForm(forms.ModelForm):
    class Meta:
        model = SupplierStatement
        fields = '__all__'
