from django.shortcuts import render
from .models import Product

# Create your views here.
def store(request, catslug=None):
    if catslug != None:
        products = Product.objects.filter(category__slug=catslug)
    else:
        products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, 'store/store.html', context)

def product_details(request, catslug=None, product_slug=None):
    product = Product.objects.get(category__slug=catslug, slug=product_slug)
    context= {
        'single_product': product
    }
    return render(request, 'store/product-details.html', context)