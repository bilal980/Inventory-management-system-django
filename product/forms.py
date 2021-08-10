from django import forms
from product.models import Product, StockOut,StockIn,PurchasedProduct,ExtraItems


class ProductForm(forms.ModelForm):
    """CustomerForm definition."""
    class Meta:
        model = Product
        fields = ('name', 'brand_name', 'unit_type',)
        # widgets = {'name': forms.TextInput(attrs={'type': "text", 'placeholder': "Name", 'class': 'form-control name', 'name': "product_name"}),
        #            'brand_name': forms.TextInput(
        #     attrs={'type': "text", 'placeholder': "brand Name (Optional)", 'class': 'form-control brand_name', 'name': "brand_name", }),
        #     'Unit Type': forms.widgets.Select(
        #     attrs={'rows': "2", 'placeholder': "Address (Optional)", 'class': 'form-control adress', 'name': "adress", }), 'shop': forms.TextInput(
        #     attrs={'type': "text", 'placeholder': "Shop Name", 'class': 'form-control shop', 'name': "shop", }),
        #     'bar_code': forms.NumberInput(
        #     attrs={'type': "text", 'placeholder': "bar_code", 'class': 'form-control bar_code', 'name': "bar_code", }), 'retail_price': forms.NumberInput(
        #     attrs={'type': "text", 'placeholder': "Retail price", 'class': 'form-control retail_price', 'name': "retail_price", }), 'consumer_price': forms.NumberInput(
        #     attrs={'type': "text", 'placeholder': "Consumer Price", 'class': 'form-control consumer_price', 'name': "consumer_price", }), 'available_item': forms.NumberInput(
        #     attrs={'type': "text", 'placeholder': "Available Items", 'class': 'form-control available_item', 'name': "available_item", }), 'purchased_item': forms.NumberInput(
        #     attrs={'type': "text", 'placeholder': "Purchased Items", 'class': 'form-control purchased_item', 'name': "purchased_item", }), }


class StockOutForm(forms.ModelForm):

    class Meta:
        model = StockOut
        fields = '__all__'


class StockDetailsForm(forms.ModelForm):
    """Form definition for StockIn."""

    class Meta:
        """Meta definition for StockInform."""

        model = StockIn
        fields ='__all__'


class PurchasedProductForm(forms.ModelForm):

    """PurchasedProductForm definition."""
    class Meta:
        """Meta definition for StockInform."""

        model = PurchasedProduct
        fields = ('__all__')
    

class ExtraItemsForm(forms.ModelForm):
    """ExtraItemsForm definition."""
    #: Define form fields here
    class Meta:
        """Meta definition for StockInform."""
        model = ExtraItems
        fields = ('__all__')
