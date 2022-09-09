from django.contrib import admin

from store.models import Product, Variation

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'slug', 'stock', 'is_available', 'category', 'date_modified'] # pour afficher les champs précisé dans le panneau admin
    prepopulated_fields = {"slug": ["product_name"]} # pour convertir le champ category_name en slug. Ex : category_name = T Shirts ===> slug = t-shirts

class VariationAdmin(admin.ModelAdmin):
  list_display = ['product', 'variation_category', 'variation_value', 'is_active']
  list_filter = ['is_active', 'variation_category']
  list_editable = ['is_active']

admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)
