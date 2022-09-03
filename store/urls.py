from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name='store'),
    path('<catslug>', views.store, name='store_by_category'),
    path('<catslug>/<product_slug>', views.product_details, name='product_details')
]
