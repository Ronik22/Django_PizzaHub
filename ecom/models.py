from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Product(models.Model):
    item = models.CharField(max_length=140)
    image = models.ImageField(upload_to='product_images', blank=True, null=True)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    discount = models.DecimalField(null=True, blank=True, max_digits=5, decimal_places=2)
    brand = models.CharField(max_length=100)
    description = models.TextField(max_length=300, null=True, blank=True)
    rating = models.CharField(default="00000", max_length=5)
    category = models.ForeignKey('Category', on_delete=models.CASCADE) 
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name="product_like", blank=True)
    buyers = models.ManyToManyField(User, related_name="product_buy", blank=True)

    def total_likes(self):
        return self.likes.count()
    
    def is_liked(self, request):
        return self.likes.filter(id=request.user.id).exists()

    def total_buyers(self):
        return self.buyers.count()

    def __str__(self):
        return f"{self.id}-{self.item}"


class Category(models.Model):
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=250, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    @property
    def get_products(self):
        return Product.objects.filter(category=self.id)

    def __str__(self):
        return f"{self.id}-{self.title}"

    class Meta:
        verbose_name = 'Categorie'