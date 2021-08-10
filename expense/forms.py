from django import forms
from expense.models import ExtraExpense

class ExtraExpenseForm(forms.ModelForm):
    class Meta:
        model = ExtraExpense
        fields = '__all__'
