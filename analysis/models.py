# Create your models here.
from django.db import models
from django.conf import settings
from inventory.models import ProductsInventory

class UserFile(models.Model):  
    product = models.ForeignKey(ProductsInventory, on_delete=models.CASCADE, related_name="analyses")  
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Add this  
    uploaded_file = models.FileField(upload_to="sentiment_csvs/")  
    cleaned_file = models.FileField(upload_to="cleaned/", blank=True, null=True)  
    keywords = models.JSONField(default=list)  
    timestamp = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"Analysis for {self.product.item_name} by {self.user.username} at {self.timestamp}"

    
    

#class UserFile(models.Model):
    #user = models.ForeignKey(User, on_delete=models.CASCADE)
   # file = models.FileField(upload_to='uploads/')
   # uploaded_at = models.DateTimeField(auto_now_add=True)
   # cleaned_file = models.FileField(upload_to='cleaned/', blank=True, null=True)  # Store cleaned file
   # uploaded_at = models.DateTimeField(auto_now_add=True)