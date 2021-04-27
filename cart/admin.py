from django.contrib import admin
from .models import Cart, Entry, Order

# Register your models here.

admin.site.register(Cart)
admin.site.register(Entry)
admin.site.register(Order)