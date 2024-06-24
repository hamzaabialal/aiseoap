from django.contrib import admin
from .models import  ShopifyAccessToken, Products, AnalyticsData
# Register your models here.
admin.site.register(ShopifyAccessToken)
admin.site.register(Products)
admin.site.register(AnalyticsData)