from django.db import models
from account.models import DatedModel

class Ledger(DatedModel):
    
    customer = models.ForeignKey(
        'customer.Customer', related_name='customer_ledger', on_delete=models.CASCADE
    )
    invoice = models.ForeignKey(
        'sale.SalesHistory', related_name='ledger_invoice',
        blank=True, null=True, on_delete=models.CASCADE
    )
    person = models.CharField(
        max_length=200, default='customer', blank=True, null=True)
    amount = models.DecimalField(
        max_digits=65, decimal_places=2, default=0, blank=True, null=True
    )
    payment = models.DecimalField(
        max_digits=65, decimal_places=2, default=0, blank=True, null=True
    )
    payment_type = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(max_length=200, blank=True, null=True)
    dated = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.customer.customer_name
