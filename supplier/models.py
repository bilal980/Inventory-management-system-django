from django.db import models
from django.db.models import Sum
# Create your models here.


class Supplier(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    phone = models.CharField(max_length=100, blank=True)
    CNIC = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name
    
    def supplier_remaining_amount(self):
        supplier_statement=self.supplier.all()
        try:
            total_amount = supplier_statement.aggregate(Sum('supplier_amount'))
            total_amount = total_amount.get('supplier_amount__sum') or 0
            total_payments = supplier_statement.aggregate(
                Sum('payment_amount'))
            total_payments = total_payments.get('payment_amount__sum') or 0
        except:
            total_amount=0
            total_payments=0
        return total_amount - total_payments


class SupplierStatement(models.Model):
    supplier = models.ForeignKey(
        Supplier, related_name='supplier', null=True, blank=True, on_delete=models.CASCADE)
    supplier_amount = models.DecimalField(
        max_digits=100, decimal_places=2, null=True, blank=True, default=0)
    payment_amount = models.DecimalField(
        max_digits=100, decimal_places=2, null=True, blank=True, default=0)
    description=models.TextField(max_length=500,null=True,blank=True)
    date=models.DateField(null=True ,blank=True)

    def __str__(self):
        return self.supplier.name
    def remaining_amount(self):
        return self.supplier_amount - self.payment_amount
