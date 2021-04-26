import json
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from ecom.models import Product
from django.shortcuts import render, get_object_or_404
from .models import Cart, Entry

# Create your views here.

@login_required
def cart(request):
    cart = get_object_or_404(Cart, user=request.user)
    # cart = get_object_or_404(Cart, user=request.user).cart_entry.all()
    products = Entry.objects.filter(cart=cart)
    context = {
        "cart":cart,
        "products": products
    }
    return render(request, 'cart/cart.html', context)


@login_required
def add_to_cart(request):
    cart = get_object_or_404(Cart, user=request.user)
    product = get_object_or_404(Product, id=request.POST.get('id'))
    cartlist = cart.cart_entry.all()

    cartp = cartlist.filter(product=product)
    if cartp:
        get_object_or_404(Entry, product=product, cart=cart).delete()

    else:
        Entry.objects.create(product=product, cart=cart, quantity=1)

    context = {
        "success": True,
    }

    if request.is_ajax():
        html = render_to_string('ecom/add_to_cart_section.html',context, request=request)
        return JsonResponse({'form':html})


@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    pdict = request.POST.get('checkoutip')
    pdict = json.loads(pdict)
    final_price = 0
    
    for keys,values in pdict.items():
        product = get_object_or_404(Product, id=int(keys))
        # Edit entry
        currp = get_object_or_404(Entry, product=product, cart=cart)
        currp.quantity = int(values)
        currp.save()
        # calc price
        final_price = final_price + product.price * int(values)

    final_price = final_price - 25
    context = {
        "pdict":pdict,
        "fprice":final_price
    }
    return render(request,'cart/checkout.html', context)