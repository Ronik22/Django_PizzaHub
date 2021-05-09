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
    products = Entry.objects.filter(cart=cart)
    context = {
        "cart":cart,
        "products": products
    }
    return render(request, 'cart/cart.html', context)


""" Add to cart or delete if present """
@login_required
def add_to_cart(request):
    cart = get_object_or_404(Cart, user=request.user)
    product = get_object_or_404(Product, id=request.POST.get('id'))
    cartlist = cart.cart_entry.all()

    cartp = cartlist.filter(product=product)
    if cartp:
        get_object_or_404(Entry, product=product, cart=cart).delete()

    else:
        if 'opt_param' in request.POST:
            Entry.objects.create(product=product, cart=cart, quantity=1, optional_parameter=str(request.POST['opt_param']))
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

    pdict = request.POST.get('checkoutip')
    cart = get_object_or_404(Cart, user=request.user)
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
def reorder(request):
    reorder = request.POST.get('checkoutip')
    reorder = reorder.replace("'","\"")
    cart = get_object_or_404(Cart, user=request.user)
    pdict = json.loads(reorder)
    final_price = 0
    
    for keys,values in pdict.items():
        product = get_object_or_404(Product, id=int(keys))
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

        if all(len(v.split()) != 0 for v in [inputName, inputMobNo, inputAddress, inputCity, inputState, inputZip, pdict, final_price]):
            pass
        else:
            return redirect('cart')
        
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
        callback_url = 'http://localhost:8000/cart/handle_payment/'
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
        current_order.order_id = order_receipt
        current_order.save()

        context = {
            "order_id" : f'ORD2PHID{current_order.id}',
            "rp_order_id" : payment['id'],
            "order" : current_order,
            "amount" : order_amount,
            "razorpay_id" : RAZORPAY_KEY_ID,
            "callback_url" : callback_url,
        }

        return render(request,'cart/payment.html', context)
    else:
        return HttpResponse("505 Not Found")

@csrf_exempt
def handle_payment(request):
    if request.method == "POST":
        try:
            payment_id = request.POST.get('razorpay_payment_id','')
            order_id = request.POST.get('razorpay_order_id','')
            signature = request.POST.get('razorpay_signature','')
            params_dict = {
                'razorpay_order_id': order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature,
            }
            try:
                order_db = Order.objects.get(razorpayid=order_id)
            except:
                return HttpResponse("505 Not Found")
            order_db.razorpaypaymentid = payment_id
            order_db.razorpaysignature = signature
            order_db.save()
            client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
            result = client.utility.verify_payment_signature(params_dict)

            if result == None:
                amount = int(float(order_db.amount) * 100)
                try:
                    client.payment.capture(payment_id, amount)
                    order_db.payment_status = 1
                    order_db.save()
                    extra = {
                        'orderid': order_db.order_id,
                    }
                    return render(request, 'cart/payment_success.html', extra)
                except:
                    order_db.payment_status = 2
                    order_db.save()
                    return render(request, 'cart/payment_failed.html')
            else:
                order_db.payment_status = 2
                order_db.save()
                return render(request, 'cart/payment_failed.html')
        except:
            return HttpResponse("505 Not Found")



""" Remove from cart only """
@login_required
def remove_from_cart(request, id):
    cart = get_object_or_404(Cart, user=request.user)
    product = get_object_or_404(Product, id=id)
    cartlist = cart.cart_entry.all()

    cartp = cartlist.filter(product=product)
    if cartp:
        get_object_or_404(Entry, product=product, cart=cart).delete()

    return redirect('cart')


def pdict_to_pstr(pdict):
    pdict = pdict.replace("'","\"")
    pdict2 = json.loads(pdict)
    newlist = ""
    for keys,values in pdict2.items():
        product = get_object_or_404(Product, id=int(keys))
        newlist = newlist + f"{pdict2[keys]} x {product.item}, "
    return newlist


def pdict_to_parray(pdict):
    pdict = pdict.replace("'","\"")
    pdict2 = json.loads(pdict)
    newlist = []
    for keys,values in pdict2.items():
        product = get_object_or_404(Product, id=int(keys))
        newlist.append([pdict2[keys], product.item, product.price])
    return newlist


@login_required
def orders(request):    
    context2 = {}
    payment_status_choices = ['SUCCESS', 'FAILURE', 'PENDING']
    orders = Order.objects.filter(user=request.user)
    for order in orders:
        productlist = pdict_to_pstr(order.items_json)
        context2[f"{order.id}"] = {
            'order_id': order.order_id,
            'items_json': order.items_json,
            'productlist': productlist,
            'amount': str(order.amount),
            'datetime_of_payment': order.datetime_of_payment.strftime('%b %d, %Y - %I:%M %p'),
            'payment_status': payment_status_choices[order.payment_status-1],
            'address': order.address,
            'phone': order.phone,
        }
    context = {}
    context['orders'] = orders
    context['orders2'] = context2
    # print(json.dumps(context2, indent = 4)  )

    return render(request, 'cart/orders.html', context)


@login_required
def generate_receipt(request, id):
    order = Order.objects.get(order_id=id)
    if order.user == request.user:
        productlist = pdict_to_parray(order.items_json)
        context = {
            'order': order,
            'productlist': productlist,
        }
        return render(request, 'cart/receipt.html', context)
    else:
        return HttpResponse("403 Forbidden")
    
    
# test function for test page to check layout 
@login_required
def testpage(request):
    return render(request, 'cart/testpage.html', {'orderid':'ORD2PHID11'})


@login_required
def order_rating(request):
    user = request.user
    order = Order.objects.get(user=user, order_id=request.POST.get('id'))
    rating = request.POST.get('rating')
    order.rating = rating
    order.save()

    context = {
        "success": True
    }
    if request.is_ajax():
        return JsonResponse(context)