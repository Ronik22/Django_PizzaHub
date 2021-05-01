from django.urls import path
from .views import cart, add_to_cart, checkout, handle_checkout, handle_payment

urlpatterns = [
    path('', cart, name="cart"),
    path('add-to-cart/', add_to_cart, name="add-to-cart"),
    path('checkout/', checkout, name="checkout"),
    path('handle_checkout/', handle_checkout, name="handle-checkout"),
    path('handle_payment/', handle_payment, name="handle-payment"),
]