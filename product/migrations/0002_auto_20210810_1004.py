# Generated by Django 3.1.2 on 2021-08-10 10:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customer', '0001_initial'),
        ('product', '0001_initial'),
        ('sale', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='stockout',
            name='invoice',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='out_invoice', to='sale.saleshistory'),
        ),
        migrations.AddField(
            model_name='stockout',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stockout_product', to='product.product'),
        ),
        migrations.AddField(
            model_name='stockout',
            name='purchased_item',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='out_purchased', to='product.purchasedproduct'),
        ),
        migrations.AddField(
            model_name='stockin',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stockin_product', to='product.product'),
        ),
        migrations.AddField(
            model_name='purchasedproduct',
            name='invoice',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='purchased_invoice', to='sale.saleshistory'),
        ),
        migrations.AddField(
            model_name='purchasedproduct',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purchased_product', to='product.product'),
        ),
        migrations.AddField(
            model_name='productdetail',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_detail', to='product.product'),
        ),
        migrations.AddField(
            model_name='extraitems',
            name='invoice',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='extraitem_invoice', to='sale.saleshistory'),
        ),
        migrations.AddField(
            model_name='claimedproduct',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='customer_claimed_items', to='customer.customer'),
        ),
        migrations.AddField(
            model_name='claimedproduct',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='claimed_product', to='product.product'),
        ),
    ]
