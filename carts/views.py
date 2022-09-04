from django.shortcuts import render, redirect

from carts.models import Cart, CartItem
from django.http import HttpResponse


# Create your views here.
from store.models import Product


def get_session_key(request):
  cart_id = request.session.session_key
  if not cart_id:
    cart_id = request.session.create()
  return cart_id

def cart(request):
  total = 0
  tax = 0
  full_total = 0
  try:
    cart = Cart.objects.get(cart_id=get_session_key(request))
    cart_items = CartItem.objects.filter(cart=cart)

    for cart_item in cart_items:
      total += cart_item.product.price * cart_item.quantity
    tax = 2*total/100
    full_total = total + tax
  except:
    pass
  
  context = {
    'cart_items': cart_items,
    'total': total,
    'tax': tax,
    'full_total': full_total
  }
  return render(request, 'store/cart.html', context)

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

  #return HttpResponse(str(cart_item.product.id) + " " + cart_item.product.product_name + " " +  str(cart_item.quantity))

  return redirect('cart')

def decrement_from_cart(request, product_id):
  product = Product.objects.get(id=product_id)
  try:
    cart = Cart.objects.get(cart_id=get_session_key(request))
    cart_item = CartItem.objects.get(cart=cart, product=product)

    if cart_item.quantity > 1:
      cart_item.quantity -= 1
      cart_item.save()
    else:
      cart_item.delete()
  except:
    pass

  return redirect('cart')

def remove_from_cart(request, product_id):
  product = Product.objects.get(id=product_id)
  try:
    cart = Cart.objects.get(cart_id=get_session_key(request))
    cart_item = CartItem.objects.get(cart=cart, product=product)
    cart_item.delete()
  except:
    pass

  return redirect('cart')

  
