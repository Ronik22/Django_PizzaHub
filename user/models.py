from cart.models import Cart
from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import CharField, IntegerField
from django.db.models.signals import post_save
from django.dispatch import receiver

""" Model for User Profile """

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200, blank=True)
    mobile_number = CharField(max_length=15, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    pin_code = models.CharField(max_length=20, blank=True) 
    state = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    full_address = models.CharField(max_length=300, blank=True)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        Cart.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()