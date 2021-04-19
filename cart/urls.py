from django.contrib import admin
from django.urls import path, include
from .views import cart

urlpatterns = [
    path('', cart, name="cart"),
]