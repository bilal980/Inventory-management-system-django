from django import forms
from customer.models import Customer


class CustomerForm(forms.ModelForm):
    """CustomerForm definition."""
    class Meta:
        model = Customer
        fields = ('customer_name', 'customer_phone', 'address', 'shop')
        widgets = {'customer_name': forms.TextInput(attrs={'type': "text", 'placeholder': "Customer Name", 'class': 'form-control customer_name', 'name': "customer_name"}), 'customer_phone': forms.TextInput(
            attrs={'type': "text", 'placeholder': "Customer Phone", 'class': 'form-control customer_phone', 'name': "customer_phone", }), 'address': forms.Textarea(
            attrs={'rows': "2", 'placeholder': "Address (Optional)", 'class': 'form-control adress', 'name': "adress", }), 'shop': forms.TextInput(
            attrs={'type': "text", 'placeholder': "Shop Name", 'class': 'form-control shop', 'name': "shop", }), }
