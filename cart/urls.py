from django.urls import path
from .views import cart, add_to_cart, checkout, handle_checkout, handle_payment, orders, reorder, remove_from_cart, generate_receipt, order_rating, testpage

urlpatterns = [
    path('', cart, name="cart"),
    path('add-to-cart/', add_to_cart, name="add-to-cart"),
    path('remove-from-cart/<id>', remove_from_cart, name="remove-from-cart"),
    path('checkout/', checkout, name="checkout"),
    path('receipt/<str:id>/', generate_receipt, name="receipt"),
    path('reorder/', reorder, name="reorder"),
    path('orders/', orders, name="orders"),
    path('handle_checkout/', handle_checkout, name="handle-checkout"),
    path('handle_payment/', handle_payment, name="handle-payment"),
    path('order-rating/', order_rating, name="order-rating"),
    path('testpage/', testpage, name="testpage"),
]