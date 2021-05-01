from django.db import models
from django.contrib.auth.models import User
from ecom.models import Product
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

""" Cart """
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=0)
    total = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} 's cart"


""" Entry """
class Entry(models.Model):
    product = models.ForeignKey(Product, null=True, on_delete=models.CASCADE, related_name="product_entry")
    cart = models.ForeignKey(Cart, null=True, on_delete=models.CASCADE, related_name="cart_entry")
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"This entry contains {self.quantity} {self.product.item}(s)."

    class Meta:
        verbose_name_plural = 'Entries'


""" Order """
class Order(models.Model):
    payment_status_choices = (
        (1, 'SUCCESS'),
        (2, 'FAILURE'),
        (3, 'PENDING'),
    )

    id = models.AutoField(primary_key=True)
    order_id = models.CharField(max_length=200, default="Unknown")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_status = models.IntegerField(choices=payment_status_choices, default=3)
    items_json = models.CharField(max_length=5000)
    name = models.CharField(max_length=90)
    address = models.CharField(max_length=500)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    amount = models.DecimalField(default=0.00, max_digits=15, decimal_places=2)
    datetime_of_payment = models.DateTimeField(default=timezone.now)
    razorpayid = models.CharField(max_length=255,default="")
    razorpaypaymentid = models.CharField(max_length=255,default="")
    razorpaysignature = models.CharField(max_length=255, default="")

    def __str__(self):
        return f"{self.id} - {self.user}"

    
@receiver(post_save, sender=Entry)
def update_cart(sender, instance, **kwargs):
    line_cost = instance.quantity * instance.product.price
    instance.cart.total += line_cost
    instance.cart.count += instance.quantity
    instance.cart.save()