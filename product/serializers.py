from rest_framework import serializers
from product.models import Product,StockIn

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields='__all__'

class StockInSerializer(serializers.ModelSerializer):
    class Meta:
        model=StockIn
        fields='__all__'

