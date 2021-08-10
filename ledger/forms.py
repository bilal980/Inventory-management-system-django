from django import forms
from ledger.models import Ledger

class LedgerForm(forms.ModelForm):
    class Meta:
        model = Ledger
        fields = "__all__"
