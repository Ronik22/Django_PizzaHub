from django.shortcuts import render
from .models import Cart, Entry

# Create your views here.

def cart(request):
    products = Entry.objects.all()
    context = {
        "products": products
    }
    return render(request, 'cart/cart.html', context)

