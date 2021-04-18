from django.db import models
from django.db.models.fields import BLANK_CHOICE_DASH

# Create your models here.

class Product(models.Model):
    item = models.CharField(max_length=140)
    image = models.ImageField(upload_to='product_images', blank=True, null=True)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    discount = models.DecimalField(null=True, blank=True, max_digits=5, decimal_places=2)
    brand = models.CharField(max_length=100)
    description = models.TextField(max_length=300, null=True, blank=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE) 
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id}-{self.item}"


class Category(models.Model):
    title = models.CharField(max_length=150)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id}-{self.title}"