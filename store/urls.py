from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name='store'),
    path('shirts/', views.store, name='shirts')
]
