from django.db import models

from store.models import Product, Variation

# Create your models here.
class Cart(models.Model):
  cart_id = models.CharField(max_length=255)
  date_add = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.cart_id


class CartItem(models.Model):
  product = models.ForeignKey(Product, on_delete=models.CASCADE)
  cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
  quantity = models.IntegerField()
  variations = models.ManyToManyField(Variation, blank=True)

  def __str__(self):
    return self.product.product_name

  def total_product_price(self):
    return self.product.price * self.quantity