from django.contrib import admin
from django.urls import path, include
from .views import cart, add_to_cart, checkout, handle_checkout, payment, paymentsuccess

urlpatterns = [
    path('', cart, name="cart"),
    path('add-to-cart/', add_to_cart, name="add-to-cart"),
    path('checkout/', checkout, name="checkout"),
    path('handle_checkout/', handle_checkout, name="handle-checkout"),
    # path('payment/<id>/', payment, name="payment"),
    path('paymentsuccess/', paymentsuccess, name="paymentsuccess"),
]