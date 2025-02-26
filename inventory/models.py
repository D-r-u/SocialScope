from django.db import models

# Create your models here.
class ProductsInventory(models.Model):
    ITEM_TYPES = [
        ('product', 'product'),
        #('service', 'service'),
        #('person', 'person')
    ]

    item_id = models.AutoField(primary_key=True)
    item_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    item_type = models.CharField(max_length=50, choices=ITEM_TYPES)
    creation_date = models.DateTimeField(auto_now_add=True)
    icon = models.ImageField(upload_to='product_icons/', blank=True, null=True)

    def __str__(self):
        return self.item_name