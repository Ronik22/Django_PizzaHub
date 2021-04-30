import json
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from ecom.models import Product
from django.shortcuts import redirect, render, get_object_or_404
from .models import Cart, Entry, Order
import razorpay
from myproject.settings import RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET

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

    final_price = final_price + 25
    context = {
        "cuser":request.user.profile,
        "pdict":pdict,
        "fprice":final_price
    }

    return render(request,'cart/checkout.html', context)


@login_required
def handle_checkout(request):
    if request.method == "POST":
        pdict = request.POST.get('pdict')
        final_price = request.POST.get('fprice')
        inputName = request.POST.get('inputName')
        inputMobNo = request.POST.get('inputMobNo')
        inputAddress = request.POST.get('inputAddress')
        inputCity = request.POST.get('inputCity')
        inputState = request.POST.get('inputState')
        inputZip = request.POST.get('inputZip')

        ####### NEED TO BE FIXED ########
        if not inputName and not inputMobNo and not inputAddress and not inputCity and not inputState and not inputZip and not pdict and not final_price:
            return redirect('cart')  ####### NEED TO BE FIXED ########
        
        neworder = Order.objects.create(
            user = request.user,
            items_json = pdict,
            name = inputName,
            phone = inputMobNo,
            address = inputAddress,
            city = inputCity,
            state = inputState,
            zip_code = inputZip,
            amount = final_price,
        )

        # PAYMENT
        current_order = neworder
        order_amount = int(float(current_order.amount) * 100)
        order_currency = 'INR'
        callback_url = 'http://localhost:8000/cart/paymentsuccess/'
        order_receipt = f'ORD2PHID{current_order.id}'
        notes = {
            'Shipping address': current_order.address,
            'Phone number': current_order.phone,
            'City': current_order.city,
            'State': current_order.state,
            'Zip code': current_order.zip_code,
        }

        client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
        payment = client.order.create(dict(amount=order_amount, currency=order_currency, receipt=order_receipt, notes=notes, payment_capture=0))
        current_order.razorpayid = payment['id']
        current_order.save()

        context = {
            "order_id" : f'ORD2PHID{current_order.id}',
            "razorpay_order_id" : payment['id'],
            "order" : current_order,
            "amount" : order_amount,
            "razorpay_id" : RAZORPAY_KEY_ID,
            "callback_url" : callback_url,
        }

        return render(request,'cart/payment.html', context)
        # return redirect('payment', id=neworder.id)
    else:
        return HttpResponse("505 Not Found")

@csrf_exempt
def paymentsuccess(request):
    return render(request,'cart/payment_success.html')


# @login_required
# def payment(request,id):
#     current_order = get_object_or_404(Order, id=id)

#     if request.method == "POST":
#         order_amount = current_order.amount * 100
#         order_currency = 'INR'
#         callback_url = 'http://localhost:8000/cart/paymentsuccess/'
#         order_receipt = f'ORD2PHID{id}'
#         notes = {
#             'Shipping address': current_order.address,
#             'Phone number': current_order.phone,
#             'City': current_order.city,
#             'State': current_order.state,
#             'Zip code': current_order.zip_code,
#         }

#         client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
#         payment = client.order.create(amount=order_amount, currency=order_currency, receipt=order_receipt, notes=notes, payment_capture=0)
#         current_order.razorpayid = payment['id']
#         current_order.save()

#     context = {
#         "order_id" : f'ORD2PHID{id}',
#         "order" : current_order,
#         "razorpay_id" : RAZORPAY_KEY_ID,
#     }
#     return render(request,'cart/payment.html', context)