from django.shortcuts import render, redirect

from carts.models import Cart, CartItem


# Create your views here.
from store.models import Product


def get_session_key(request):
  cart_id = request.session.session_key
  if not cart_id:
    cart_id = request.session.create()
  return cart_id

def cart(request):
  try:
    cart = Cart.objects.get(cart_id=get_session_key(request))
    cart_items = CartItem.objects.filter()
  except:
    pass
  return render(request, 'store/cart.html')

def add_to_cart(request, product_id):
  product = Product.objects.get(id=product_id)
  try:
    cart = Cart.objects.get(cart_id=get_session_key(request))
  except Cart.DoesNotExist:
    cart = Cart.objects.create(cart_id=get_session_key(request))
  cart.save()

  try:
    cart_item = CartItem.objects.get(cart=cart, product=product)
    cart_item.quantity += 1
  except CartItem.DoesNotExist:
    cart_item  = CartItem.objects.create(cart=cart, quantity=1, product=product)
  cart_item.save()

  return redirect('cart')

