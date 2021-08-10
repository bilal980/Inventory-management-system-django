from sale.models import SalesHistory
from django import forms

class SaleForm(forms.ModelForm):
    """Form definition for Sale."""

    class Meta:
        """Meta definition for Saleform."""
        model = SalesHistory
        fields = '__all__'
