from django.contrib import admin
from django.urls import path, include
from .views import contact_us, home, menu, LikeView, wishlist, remove_from_wishlist, search, about, product_details

urlpatterns = [
    path('', home, name="home"),
    path('about/', about, name="about"),
    path('menu/', menu, name="menu"),
    path('contact_us/', contact_us, name="contact-us"),
    path('wishlist/', wishlist, name="wishlist"),
    path('search/', search, name='search'),
    path('product/remove-like/', remove_from_wishlist, name="wishlist-remove"),
    path('product/like/', LikeView, name='product-like'),
    path('product/<int:id>/details/', product_details, name='product-details'),
]