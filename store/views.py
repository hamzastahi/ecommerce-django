from django.shortcuts import render
from .models import Product

# Create your views here.
def store(request, catslug=None):
    if catslug != None:
        products = Product.objects.filter(category__slug=catslug)
    else:
        products = Product.objects.all()
    product_count = products.count()
    context = {
        'products': products,
        'product_count': product_count
    }
    return render(request, 'store/store.html', context)

def product_details(request, catslug=None, product_slug=None):
    product = Product.objects.get(category__slug=catslug, slug=product_slug)
    variations_color = product.variation_set.filter(variation_category="color")
    variations_size = product.variation_set.filter(variation_category="size")
    context= {
        'single_product': product,
        'variations_color': variations_color,
        'variations_size' : variations_size
    }
    return render(request, 'store/product-details.html', context)