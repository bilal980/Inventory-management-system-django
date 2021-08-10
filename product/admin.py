from django.contrib import admin
from .models import PurchasedProduct, Product, ProductDetail, StockIn, StockOut, ClaimedProduct, ExtraItems
# Register your models here.
admin.site.register(PurchasedProduct)
admin.site.register(Product)
admin.site.register(ProductDetail)
admin.site.register(StockIn)
admin.site.register(StockOut)
admin.site.register(ClaimedProduct)
admin.site.register(ExtraItems)
