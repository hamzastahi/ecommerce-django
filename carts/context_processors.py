from .models import CartItem, Cart
from .views import get_session_key

def cart_count(request):
  cart_items_count = 0
  try:
    cart = Cart.objects.get(cart_id=get_session_key(request))
    cart_items = CartItem.objects.filter(cart=cart)
    for cart_item in cart_items:
      cart_items_count += cart_item.quantity
  except Cart.DoesNotExist:
    pass

  return {'cart_count': cart_items_count}