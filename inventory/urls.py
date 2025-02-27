from django.urls import path
from .views import *

urlpatterns = [
    path('add-product/', add_product, name='add_product'),
    path('add-product/', add_product, name='add_product'),
    path('inventory/', product_list, name='product-list'),
    path('inventory/delete/<int:product_id>/', delete_inventory, name='delete-inventory'),
]
