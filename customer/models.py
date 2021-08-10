from django.db import models

# Create your models here.

class Customer(models.Model):
  
    customer_types=(('Customer','customer'),('Wholesale','wholesale'))
    customer_name = models.CharField(max_length=200)
    customer_phone = models.CharField(max_length=20, blank=True, null=True)
    customer_type = models.CharField(
        max_length=200,choices=customer_types, default='customer', blank=True, null=True)
    address = models.TextField(max_length=500, blank=True, null=True)
    shop = models.CharField(max_length=200, blank=True, null=True)
