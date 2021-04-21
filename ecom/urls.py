from django.contrib import admin
from django.urls import path, include
from .views import home, menu, LikeView

urlpatterns = [
    path('', home, name="home"),
    path('menu/', menu, name="menu"),
    path('product/like/', LikeView, name='product-like'),
]