from itertools import product
from django.shortcuts import *

from store.models import Product
from . import urls

def home(request):
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, 'home.html', context)