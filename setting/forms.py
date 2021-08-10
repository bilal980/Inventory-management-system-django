from django import forms
from setting.models import BusinessDetail

class BusinessDetailForm(forms.ModelForm):
    """Form definition for BusinessDetail."""
    class Meta:
        """Meta definition for BusinessDetailform."""
        model = BusinessDetail
        fields = ('__all__')
