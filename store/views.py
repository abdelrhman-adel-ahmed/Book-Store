from django.db.models import Count, Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from .models import Category, Product


def product_all(request):
    """
    instead of fetching the products like that and then go fetch every featured  image associated with
    each product each image fetch will be in a diffrent query we do prefetch_related and that fetch all the
    images associated with the product in one query
    products = Product.objects.all()
    e.x:
     select ... from store_product
     then
     select ...from store_productimage where product_id =1
     select ...from store_productimage where product_id =2 ...
    * what happen instead when we using prefetch_related is :
    select ... from store_product where is_active=True
    select ... from store_productimage where product_id IN (1,2,...)
    see the docs :https://docs.djangoproject.com/en/3.1/ref/models/querysets/#prefetch-related
    """
    products = Product.objects.prefetch_related("product_image").filter(is_active=True)
    context = {"products": products}
    return render(request, "store/index.html", context)


def category_list(request, slug=None):
    category = get_object_or_404(Category, slug=slug)
    # collect the category we get pass in the slug and all the decendants categorys of that category including that category it self
    # e.x cars category get passed --> then all decendatn categorys will get passed too to the filter function
    products = Product.objects.filter(category__in=Category.objects.get(name=slug).get_descendants(include_self=True))
    context = {"category": category, "products": products}

    return render(request, "store/category.html", context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    product_wichlist = product.user_wishlist.filter(id=request.user.id).exists()
    context = {"product": product, "product_wichlist": product_wichlist}
    return render(request, "store/detail.html", context)


def get_query_product(query=None):
    product = Product.objects.all()
    queryset = product.filter(Q(title__icontains=query) | Q(description__icontains=query)).distinct()
    return queryset


def search(request):
    product = Product.objects.all()
    # if no value passed to search set deffult of nothing search=""
    query = ""
    if request.GET:
        query = request.GET.get("search", "")
        print("ss")
    queryset = get_query_product(query)
    context = {"products": queryset}
    return render(request, "store/index.html", context)
