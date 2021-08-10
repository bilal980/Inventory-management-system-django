from rest_framework import serializers
# Create your serializers here.


class Ledger(serializers.Serializer):
    serializers.
    customer = serializers.ForeignKey(
        'customer.Customer', related_name='customer_ledger', on_delete=serializers.CASCADE
    )
    invoice = serializers.ForeignKey(
        'sale.SalesHistory', related_name='ledger_invoice',
        blank=True, null=True, on_delete=serializers.CASCADE
    )
    person = serializers.CharField(
        max_length=200, default='customer', blank=True, null=True)
    amount = serializers.DecimalField(
        max_digits=65, decimal_places=2, default=0, blank=True, null=True
    )
    payment = serializers.DecimalField(
        max_digits=65, decimal_places=2, default=0, blank=True, null=True
    )
    payment_type = serializers.CharField(max_length=200, blank=True, null=True)
    description = serializers.TextField(max_length=200, blank=True, null=True)
    dated = serializers.DateField(null=True, blank=True)
    serializers.