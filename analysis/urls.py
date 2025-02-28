from django.urls import path
from .views import *

urlpatterns = [
    path('sentiment/<int:product_id>/', sentiment_analysis, name='sentiment-analysis'),
    path('analysis/<int:product_id>/', start_analysis, name='start-analysis'),
    path('sentiment/<int:product_id>/upload/', upload_csv, name='upload-csv'),
    path('sentiment/<int:product_id>/keywords/', select_keywords, name='select-keywords'),
]
