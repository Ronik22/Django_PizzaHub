from django.shortcuts import render
from .models import Product, Category

# Create your views here.

def home(request):
    products = Product.objects.all()
    context = {
        "products": products
    }
    return render(request, 'ecom/home.html', context)

def menu(request):
    products = Product.objects.all()
    context = {
        "products": products
    }
    return render(request, 'ecom/menu.html', context)