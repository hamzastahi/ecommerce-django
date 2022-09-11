from django.shortcuts import render, redirect

from carts.models import Cart, CartItem
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


# Create your views here.
from store.models import Product, Variation


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
    if request.user.is_authenticated:
      cart_items = CartItem.objects.filter(user=request.user)
    else:
      cart = Cart.objects.get(cart_id=get_session_key(request))
      cart_items = CartItem.objects.filter(cart=cart)

    for cart_item in cart_items:
      total += cart_item.product.price * cart_item.quantity
    tax = 2*total/100
    full_total = total + tax
  except:
    cart = Cart.objects.create(cart_id=get_session_key(request))
    cart_items = CartItem.objects.filter(cart=cart)
    pass
  
  context = {
    'cart_items': cart_items,
    'total': total,
    'tax': tax,
    'full_total': full_total
  }
  return render(request, 'store/cart.html', context)

def add_to_cart(request, product_id):
  current_user = request.user
  if current_user.is_authenticated:
    product_variations = []
    if request.method == 'POST':
      for item in request.POST:
        if item != 'csrfmiddlewaretoken':
          key = item
          value = request.POST[item]

          variation = Variation.objects.get(variation_category=key, variation_value=value)
          # 1/ ajouter les variations souhaités dans la cart qui concernent le produit selectionné
          product_variations.append(variation)

          print(variation.variation_category + ' : ' + variation.variation_value)
    product = Product.objects.get(id=product_id)

    try:
      # 2/ get all cart_items with same product
      cart_items_for_same_product = CartItem.objects.filter(user=current_user, product=product)

      #3/ ajouter toutes les variations d'un produit sur une liste
      existing_variations_list = []
      ids = []
      for item in cart_items_for_same_product:
        existing_vars = item.variations.all()
        existing_variations_list.append(list(existing_vars))
        ids.append(item.id)
      
      if product_variations in existing_variations_list:
        index = existing_variations_list.index(product_variations)
        item_id = ids[index]
        cart_item = CartItem.objects.get(user=current_user, product=product, id=item_id)
        cart_item.quantity += 1
        cart_item.save()
      else:
        cart_item = CartItem.objects.create(user=current_user, product=product, quantity=1)
        for var in product_variations:
          cart_item.variations.add(var)
        cart_item.save()

      #cart_item.quantity += 1
    except CartItem.DoesNotExist:
      cart_item  = CartItem.objects.create(user=current_user, quantity=1, product=product)
      for var in product_variations:
        cart_item.variations.add(var)
      cart_item.save()
    #return HttpResponse(str(cart_item.product.id) + " " + cart_item.product.product_name + " " +  str(cart_item.quantity))

    return redirect('cart')
  else:
    product_variations = []
    if request.method == 'POST':
      for item in request.POST:
        if item != 'csrfmiddlewaretoken':
          key = item
          value = request.POST[item]

          variation = Variation.objects.get(variation_category=key, variation_value=value)
          # 1/ ajouter les variations souhaités dans la cart qui concernent le produit selectionné
          product_variations.append(variation)

          print(variation.variation_category + ' : ' + variation.variation_value)
    product = Product.objects.get(id=product_id)
    try:
      cart = Cart.objects.get(cart_id=get_session_key(request))
    except Cart.DoesNotExist:
      cart = Cart.objects.create(cart_id=get_session_key(request))
    cart.save()

    try:
      # 2/ get all cart_items with same product
      cart_items_for_same_product = CartItem.objects.filter(cart=cart, product=product)

      #3/ ajouter toutes les variations d'un produit sur une liste
      existing_variations_list = []
      ids = []
      for item in cart_items_for_same_product:
        existing_vars = item.variations.all()
        existing_variations_list.append(list(existing_vars))
        ids.append(item.id)
      
      if product_variations in existing_variations_list:
        index = existing_variations_list.index(product_variations)
        item_id = ids[index]
        cart_item = CartItem.objects.get(cart=cart, product=product, id=item_id)
        cart_item.quantity += 1
        cart_item.save()
      else:
        cart_item = CartItem.objects.create(cart=cart, product=product, quantity=1)
        for var in product_variations:
          cart_item.variations.add(var)
        cart_item.save()

      #cart_item.quantity += 1
    except CartItem.DoesNotExist:
      cart_item  = CartItem.objects.create(cart=cart, quantity=1, product=product)
      for var in product_variations:
        cart_item.variations.add(var)
      cart_item.save()
    #return HttpResponse(str(cart_item.product.id) + " " + cart_item.product.product_name + " " +  str(cart_item.quantity))

    return redirect('cart')

def decrement_from_cart(request, product_id, cart_id):
  product = Product.objects.get(id=product_id)
  current_user = request.user
  try:
    if current_user.is_authenticated:
      cart_item = CartItem.objects.get(user=current_user, product=product)
    else:
      cart = Cart.objects.get(cart_id=get_session_key(request))
      cart_item = CartItem.objects.get(cart=cart, product=product, id=cart_id)

    if cart_item.quantity > 1:
      cart_item.quantity -= 1
      cart_item.save()
    else:
      cart_item.delete()
  except:
    pass

  return redirect('cart')

def remove_from_cart(request, product_id, cart_id):
  product = Product.objects.get(id=product_id)
  current_user = request.user
  try:
    if current_user.is_authenticated:
      cart_item = CartItem.objects.get(user=current_user, product=product)
    else:
      cart = Cart.objects.get(cart_id=get_session_key(request))
      cart_item = CartItem.objects.get(cart=cart, product=product, id=cart_id)
    cart_item.delete()
  except:
    pass

  return redirect('cart')

@login_required(login_url='login')
def checkout(request):
  current_user = request.user
  try:
    if current_user.is_authenticated:
      cart_items = CartItem.objects.filter(user=current_user)
    else:
      cart = Cart.objects.get(cart_id=get_session_key(request))
      cart_items = CartItem.objects.filter(cart=cart)
  except:
    if not current_user.is_authenticated:
      cart = Cart.objects.create(cart_id=get_session_key(request))
      cart_items = CartItem.objects.filter(cart=cart)
    pass

  context = {
    'cart_items': cart_items
  }
  return render(request, 'store/checkout.html', context)