from django.contrib import admin
from .models import  ShopifyAccessToken, Products
# Register your models here.
admin.site.register(ShopifyAccessToken)
admin.site.register(Products)