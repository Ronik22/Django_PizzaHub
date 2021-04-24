from django.contrib import admin
from django.urls import path, include
from .views import cart, add_to_cart

urlpatterns = [
    path('', cart, name="cart"),
    path('add-to-cart/', add_to_cart, name="add-to-cart"),
]