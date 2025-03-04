from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('sentiment/<int:product_id>/', sentiment_analysis, name='sentiment-analysis'),
    path('analysis/<int:product_id>/', start_analysis, name='start-analysis'),
    path('sentiment/<int:product_id>/upload/', upload_csv, name='upload-csv'),
    path('process-file/<int:file_id>/', process_file, name='process-file'),
#    path('sentiment/<int:product_id>/keywords/', select_keywords, name='select-keywords'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
