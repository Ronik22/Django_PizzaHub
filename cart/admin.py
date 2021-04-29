from django.contrib import admin
from .models import Cart, Entry, Order

# Register your models here.

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("user", "count", "total")


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ("product", "cart", "quantity")
    list_filter = ("cart", )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "datetime_of_payment")
    list_filter = ("user", "datetime_of_payment",)