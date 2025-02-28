from django.db import models
from inventory.models import ProductsInventory

# Create your models here.
class SentimentAnalysis(models.Model):
    product = models.ForeignKey(ProductsInventory, on_delete=models.CASCADE, related_name="analyses")
    uploaded_file = models.FileField(upload_to='sentiment_csvs/', blank=True, null=True)
    keywords = models.JSONField(default=list)  # Store selected keywords
    result = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Analysis for {self.product.item_name} at {self.timestamp}"