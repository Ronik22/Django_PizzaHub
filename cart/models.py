from django.db import models
from django.contrib.auth.models import User
from ecom.models import Product

# Create your models here.

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=0)
    total = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} 's cart"



class Entry(models.Model):
    product = models.ForeignKey(Product, null=True, on_delete=models.CASCADE, related_name="product_entry")
    cart = models.ForeignKey(Cart, null=True, on_delete=models.CASCADE, related_name="cart_entry")
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"This entry contains {self.quantity} {self.product.item}(s)."

    class Meta:
        verbose_name = 'Entrie'