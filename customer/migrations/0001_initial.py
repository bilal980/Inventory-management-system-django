# Generated by Django 3.1.2 on 2021-08-10 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_name', models.CharField(max_length=200)),
                ('customer_phone', models.CharField(blank=True, max_length=20, null=True)),
                ('customer_type', models.CharField(blank=True, choices=[('Customer', 'customer'), ('Wholesale', 'wholesale')], default='customer', max_length=200, null=True)),
                ('address', models.TextField(blank=True, max_length=500, null=True)),
                ('shop', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
    ]
