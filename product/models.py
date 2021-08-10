from django.db import models
# Create your models here.
from account.models import DatedModel
from django.db.models import Sum

class Product(models.Model):
    """Model definition for Product."""
    UNIT_TYPE_KG = 'Kilogram'
    UNIT_TYPE_GRAM = 'Gram'
    UNIT_TYPE_LITRE = 'Litre'
    UNIT_TYPE_QUANTITY = 'Quantity'
    UNIT_TYPES = (
        (UNIT_TYPE_KG, 'Kilogram'),
        (UNIT_TYPE_GRAM, 'Gram'),
        (UNIT_TYPE_LITRE, 'Litre'),
        (UNIT_TYPE_QUANTITY, 'Quantity'),
    )
    unit_type = models.CharField(
        choices=UNIT_TYPES, default=UNIT_TYPE_QUANTITY, blank=True, null=True, max_length=200)
    name = models.CharField(max_length=100, unique=True)
    brand_name = models.CharField(max_length=200, blank=True, null=True)
    bar_code = models.CharField(
        max_length=100, unique=True, blank=True, null=True)
    
    def __str__(self):
        return self.name

    def total_items(self):
        try:
            obj_stock_in = self.stockin_product.aggregate(Sum("quantity"))
            stock_in = float(obj_stock_in.get('quantity__sum'))
        except:
            stock_in = 0
        return stock_in
    
    def product_available_items(self):
        try:
            obj_stock_in = self.stockin_product.aggregate(Sum('quantity'))
            stock_in = float(obj_stock_in.get('quantity__sum'))
        except:
            stock_in = 0

        try:
            obj_stock_out = self.stockout_product.aggregate( Sum('stock_out_quantity'))
            stock_out = float(obj_stock_out.get('stock_out_quantity__sum'))
        except:
            stock_out = 0
        return stock_in - stock_out

    def product_purchased_items(self):
        try:
            obj_stock_out = self.stockout_product.aggregate(
                Sum('stock_out_quantity'))
            stock_out = float(obj_stock_out.get('stock_out_quantity__sum'))
        except:
            stock_out = 0
        return stock_out

    def total_num_of_claimed_items(self):
        obj = self.claimed_product.aggregate(Sum('claimed_items'))
        return obj.get('claimed_items__sum')

def int_to_bin(value):
    return bin(value)[2:]

def bin_to_int(value):
    return int(value, base=2)

class StockIn(models.Model):
    product = models.ForeignKey(
        Product, related_name='stockin_product', on_delete=models.CASCADE
    )
    quantity = models.CharField(max_length=100, blank=True, null=True)
    price_per_item = models.DecimalField(
        max_digits=65, decimal_places=2, default=0,
        help_text="Selling Price for a Single Item"
    )
    total_amount = models.DecimalField(
        max_digits=65, decimal_places=2, default=0, blank=True, null=True
    )
    buying_price_item = models.DecimalField(
        max_digits=65, decimal_places=2, default=0, blank=True, null=True,
        help_text='Buying Price for a Single Item'
    )
    total_buying_amount = models.DecimalField(
        max_digits=65, decimal_places=2, default=0, blank=True, null=True
    )

    dated_order = models.DateField(blank=True, null=True)
    stock_expiry = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.product.name

class ProductDetail(DatedModel):
    product = models.ForeignKey(
        Product, related_name='product_detail', on_delete=models.CASCADE
    )
    retail_price = models.DecimalField(
        max_digits=65, decimal_places=2, default=0
    )
    consumer_price = models.DecimalField(
        max_digits=65, decimal_places=2, default=0
    )
    available_item = models.IntegerField(default=1)
    purchased_item = models.IntegerField(default=0)

class PurchasedProduct(DatedModel):
    product = models.ForeignKey(
        Product, related_name='purchased_product', on_delete=models.CASCADE
    )
    invoice = models.ForeignKey(
        'sale.SalesHistory', related_name='purchased_invoice',
        blank=True, null=True, on_delete=models.CASCADE
    )
    quantity = models.DecimalField(
        max_digits=65, decimal_places=2, default=1, blank=True, null=True
    )
    price = models.DecimalField(
        max_digits=65, decimal_places=2, default=0, blank=True, null=True
    )
    discount_percentage = models.DecimalField(
        max_digits=65, decimal_places=2, default=0, blank=True, null=True
    )
    purchase_amount = models.DecimalField(
        max_digits=65, decimal_places=2, default=0, blank=True, null=True
    )

class ExtraItems(DatedModel):

    invoice = models.ForeignKey(
        'sale.SalesHistory', related_name='extraitem_invoice',
        blank=True, null=True, on_delete=models.CASCADE
    )
    item_name = models.CharField(
        max_length=100, blank=True, null=True)
    quantity = models.CharField(
        max_length=100, blank=True, null=True)
    price = models.DecimalField(
        max_digits=65, decimal_places=2, default=0, blank=True, null=True)
    discount_percentage = models.DecimalField(
        max_digits=65, decimal_places=2, default=0, blank=True, null=True)
    total = models.DecimalField(
        max_digits=65, decimal_places=2, default=0, blank=True, null=True)

class ClaimedProduct(DatedModel):
    product = models.ForeignKey(
        Product, related_name='claimed_product', on_delete=models.CASCADE)
    customer = models.ForeignKey(
        'customer.Customer', related_name='customer_claimed_items',
        null=True, blank=True, on_delete=models.CASCADE
    )
    claimed_items = models.IntegerField(
        default=1, verbose_name='No. of Claimed Items')
    claimed_amount = models.DecimalField(
        max_digits=65, decimal_places=2, default=0, blank=True, null=True)

class StockOut(models.Model):
    product = models.ForeignKey(
        Product, related_name='stockout_product', on_delete=models.CASCADE
    )
    invoice = models.ForeignKey(
        'sale.SalesHistory', related_name='out_invoice',
        blank=True, null=True, on_delete=models.CASCADE
    )
    purchased_item = models.ForeignKey(
        PurchasedProduct, related_name='out_purchased',
        blank=True, null=True, on_delete=models.CASCADE
    )
    stock_out_quantity = models.CharField(
        max_length=100, blank=True, null=True)
    selling_price = models.DecimalField(
        max_digits=65, decimal_places=2, default=0, blank=True, null=True
    )
    buying_price = models.DecimalField(
        max_digits=65, decimal_places=2, default=0, blank=True, null=True
    )
    dated = models.DateField(blank=True, null=True)
