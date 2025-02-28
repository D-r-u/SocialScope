from django.db import models
from inventory.models import ProductsInventory

# Create your models here.
class UserFile(models.Model):
    product = models.ForeignKey(ProductsInventory, on_delete=models.CASCADE, related_name="analyses")
    uploaded_file = models.FileField(upload_to='sentiment_csvs/', blank=True, null=True)
    keywords = models.JSONField(default=list)  # Store selected keywords
    cleaned_file = models.FileField(upload_to='cleaned/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Analysis for {self.product.item_name} at {self.timestamp}"

#class UserFile(models.Model):
    #user = models.ForeignKey(User, on_delete=models.CASCADE)
   # file = models.FileField(upload_to='uploads/')
   # uploaded_at = models.DateTimeField(auto_now_add=True)
   # cleaned_file = models.FileField(upload_to='cleaned/', blank=True, null=True)  # Store cleaned file
   # uploaded_at = models.DateTimeField(auto_now_add=True)