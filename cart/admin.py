from django.contrib import admin
from django.contrib.auth.models import User
from .models import Cart, Entry, Order
from django.db import models

# Register your models here.

class EntryInline(admin.TabularInline):
    model = Entry
    extra = 0

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("user", "delivery_charges",)
    fieldsets = (
        (None, {
            'fields': ('user', 'delivery_charges',)
        }),
    )

    inlines = [
        EntryInline,
    ]



@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ("product", "cart", "quantity")
    list_filter = ("cart", )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("order_id", "user", "datetime_of_payment")
    list_filter = ("user", "datetime_of_payment",)