from cart.models import Cart
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category, Contact
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.http import JsonResponse

# Create your views here.

def home(request):
    products = Product.objects.all().order_by('-rating')[:3]
    context = {
        "products": products
    }
    return render(request, 'ecom/home.html', context)


def about(request):
    return render(request, 'ecom/about.html')


def menu(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    context = {}
    context["products"] = {}
    already_liked = []
    in_cart = []

    if request.user.is_authenticated:
        cart = get_object_or_404(Cart, user=request.user).cart_entry.all()

        for p in products:
            context["products"][p.pk] = {}
            context["products"][p.pk]["item"] = p
            context["products"][p.pk]["is_liked"] = p.likes.filter(id=request.user.id).exists()

            # cart items
            cartp = cart.filter(product=p)
            if cartp:
                in_cart.append(p)
            if p.likes.filter(id=request.user.id).exists():
                already_liked.append(p)

    context["categories"] = categories
    context["already_liked"] = already_liked
    context["in_cart"] = in_cart
    # print(context)

    return render(request, 'ecom/menu.html', context)


""" Product Like """
@login_required
def LikeView(request):
    context = {}
    products = Product.objects.all()
    categories = Category.objects.all()
    already_liked = []
    for p in products:
        if p.likes.filter(id=request.user.id).exists():
            already_liked.append(p)

    product = get_object_or_404(Product, id=request.POST.get('id'))

    if product.likes.filter(id=request.user.id).exists():
        product.likes.remove(request.user)
        already_liked.remove(product)
    else:
        product.likes.add(request.user)
        already_liked.append(product)

    context["categories"] = categories
    context["already_liked"] = already_liked
    # context["product.id"] = product.id

    if request.is_ajax():
        html = render_to_string('ecom/like_section.html',context, request=request)
        return JsonResponse({'form':html})


@login_required
def wishlist(request):
    user = request.user
    likes = user.product_like.all()
    cart = get_object_or_404(Cart, user=request.user).cart_entry.all()
    in_cart = []

    for p in likes:
        # cart items
        cartp = cart.filter(product=p)
        if cartp:
            in_cart.append(p)

    context = {
        "wishlist": likes,
        "in_cart":in_cart
    }
    return render(request, 'ecom/wishlist.html', context)


@login_required
def remove_from_wishlist(request):
    user = request.user
    product = get_object_or_404(Product, id=request.POST.get('id'))
    likes = user.product_like.all()
    product.likes.remove(user)

    context = {
        "wishlist": user.product_like.all()
    }
    if request.is_ajax():
        html = render_to_string('ecom/wishlist_section.html',context, request=request)
        return JsonResponse({'form':html})



""" Search by product or category """
def search(request):
    query = request.GET['query']
    if len(query) >= 150 or len(query) < 1:
        res = Product.objects.none()
    elif len(query.strip()) == 0:
        res = Product.objects.none()
    else:
        allprod = Product.objects.filter(item__icontains=query)
        allcatg = Category.objects.filter(title__icontains=query)
        if allcatg:
            pincatg = allcatg[0].get_products.all()
            res = allprod.union(pincatg)
        else:
            res = allprod

    # CART and LIKE
    in_cart = []
    already_liked = []
    if request.user.is_authenticated:
        cart = get_object_or_404(Cart, user=request.user).cart_entry.all()
        for p in res:
            cartp = cart.filter(product=p)
            if cartp:
                in_cart.append(p)
            if p.likes.filter(id=request.user.id).exists():
                already_liked.append(p)
    
    context = {
        'res': res,
        'in_cart': in_cart,
        "already_liked": already_liked
    }
    return render(request, 'ecom/search_results.html', context)


def contact_us(request):
    name = request.POST.get('fname')
    message = request.POST.get('message')
    email = request.POST.get('email')
    Contact.objects.create(name=name, message=message, email=email)
    return redirect(request.META['HTTP_REFERER']+'#footerCtf')


def product_details(request, id):
    product = Product.objects.get(id=id)
    in_cart = []
    already_liked = []
    if request.user.is_authenticated:
        cart = get_object_or_404(Cart, user=request.user).cart_entry.all()
        cartp = cart.filter(product=product)
        if cartp:
            in_cart.append(product)
        if product.likes.filter(id=request.user.id).exists():
            already_liked.append(product)

    context = {
        "product":product,
        "already_liked":already_liked,
        "in_cart":in_cart,
    }
    return render(request, 'ecom/product_details.html', context)