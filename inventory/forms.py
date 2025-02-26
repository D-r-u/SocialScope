from django import forms
from .models import ProductsInventory

class ProductsInventoryForm(forms.ModelForm):
    class Meta:
        model = ProductsInventory
        fields = ['item_name', 'description', 'item_type', 'icon']
