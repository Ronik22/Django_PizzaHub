from django.contrib import admin
from .models import Contact, Product, Category

# Register your models here.

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Contact)
