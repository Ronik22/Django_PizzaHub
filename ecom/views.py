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
    liked = False
    if product.likes.filter(id=request.user.id).exists():
        product.likes.remove(request.user)
        liked = False
        already_liked.remove(product)
    else:
        product.likes.add(request.user)
        liked = True
        already_liked.append(product)

    context["categories"] = categories
    context["already_liked"] = already_liked
    # context["product.id"] = product.id

    if request.is_ajax():
        html = render_to_string('ecom/like_section.html',context, request=request)
        return JsonResponse({'form':html})