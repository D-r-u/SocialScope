from django.urls import path
from .views import *

urlpatterns = [
    path('add-product/', add_product, name='add_product'),
    path('add-product/', add_product, name='add_product'),
    path('inventory/', product_list, name='product-list'),
    path('inventory/delete/<int:product_id>/', delete_inventory, name='delete-inventory'),
    path('sentiment/<int:product_id>/', sentiment_analysis, name='sentiment-analysis'),
    path('analysis/<int:product_id>/', start_analysis, name='start-analysis'),
    path('sentiment/<int:product_id>/upload/', upload_csv, name='upload-csv'),
    path('sentiment/<int:product_id>/keywords/', select_keywords, name='select-keywords'),
]
