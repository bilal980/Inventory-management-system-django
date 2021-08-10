from rest_framework import serializers


class CustomerSerializer(serializers.Serializer):
 
    customer_types = (('Customer', 'customer'), ('Wholesale', 'wholesale'))
    customer_name = serializers.CharField(max_length=200)
    customer_phone = serializers.CharField(
        max_length=20, blank=True, null=True)
    customer_type = serializers.CharField(
        max_length=200, choices=customer_types, default='customer', blank=True, null=True)
    address = serializers.TextField(max_length=500, blank=True, null=True)
    shop = serializers.CharField(max_length=200, blank=True, null=True)
