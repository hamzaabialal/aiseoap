

from django.urls import path
from . import views

urlpatterns = [
    path('fetch/', views.FetchProductsFromShopify.as_view(), name="shopify_profucts"),
    path("list/", views.ListProducts.as_view(), name="list_products"),
    path("reterive/<int:pk>/", views.ReteriveProduct.as_view(), name="reterive_product"),
    path("analytics/", views.FetchAnalyticsDataFromShopify.as_view(), name="analytics"),
   ]
