from django.contrib import admin
from django.urls import path, include, re_path
from .views import InitCart, UpdateCart


urlpatterns = [

    path('', InitCart.as_view(), name='init-cart'),
    path('update/', UpdateCart.as_view(), name='update-cart')






]