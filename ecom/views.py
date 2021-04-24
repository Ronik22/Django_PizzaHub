from django.shortcuts import render, get_object_or_404
from .models import Product, Category
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.http import JsonResponse

# Create your views here.

def home(request):
    products = Product.objects.all()
    context = {
        "products": products
    }
    return render(request, 'ecom/home.html', context)


def menu(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    context = {}
    context["products"] = {}
    already_liked = []

    for p in products:
        context["products"][p.pk] = {}
        context["products"][p.pk]["item"] = p
        context["products"][p.pk]["is_liked"] = p.likes.filter(id=request.user.id).exists()
        if p.likes.filter(id=request.user.id).exists():
            already_liked.append(p)

    context["categories"] = categories
    context["already_liked"] = already_liked
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
    context = {
        "wishlist": likes
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
        # allcatg = Category.objects.filter(title__icontains=query)[0].Category.all()
        # res = allprod.union(allcatg)
        res = allprod
    
    params = {'res': res}
    return render(request, 'ecom/search_results.html', params)

