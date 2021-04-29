from django.contrib import admin
from .models import Contact, Product, Category

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "updated")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("item", "category", "updated")
    list_filter = ("category", )


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "datetime")
    list_filter = ("name", "datetime",)
