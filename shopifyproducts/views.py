import requests
from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from Aiseoapp import settings
from management.models import StoreManagement
from shopifyproducts.models import Products, ShopifyAccessToken
from shopifyproducts.serializers import ProductsSerializer


# Create your views here.
class FetchProductsFromShopify(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        store = StoreManagement.objects.get(user=request.user)
        access_token = ShopifyAccessToken.objects.get(user=request.user).access_token
        shopify_url = f"https://{store.store_name}.myshopify.com/admin/api/2021-07/products.json"
        headers = {
            "X-Shopify-Access-Token": access_token
        }
        response = requests.get(shopify_url, headers=headers)
        if response.status_code == 200:
            products = response.json().get("products", [])
            for product_data in products:
                product, created = Products.objects.update_or_create(
                    shopify_product_id=product_data["id"],
                    defaults={
                        "user": request.user,
                        "title": product_data["title"],
                        "description": product_data["body_html"],
                        "price": product_data["variants"][0]["price"],
                        "inventory_quantity": product_data["variants"][0]["inventory_quantity"],
                        "product_id": product_data["id"],
                        "vendor": product_data["vendor"],
                        "product_type": product_data["product_type"],
                        "created_at": product_data["created_at"],
                        "handle": product_data["handle"],
                        "updated_at": product_data["updated_at"],
                        "published_at": product_data["published_at"],
                        "template_suffix": product_data["template_suffix"],
                        "published_scope": product_data["published_scope"],
                        "tags": product_data["tags"],
                        "status": product_data["status"],
                        "admin_graphql_api_id": product_data["admin_graphql_api_id"],
                        "variants": product_data["variants"],




                    }
                )
            return Response({"message": "Products fetched and stored successfully."}, status=200)
        return Response({"error": "Failed to fetch products from Shopify."}, status=response.status_code)


class ListProducts(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    queryset = Products
    serializer_class =ProductsSerializer

    def get_queryset(self):
        return Products.objects.filter(user=self.request.user)

class ReteriveProduct(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    queryset = Products
    serializer_class = ProductsSerializer

    def get_queryset(self):
        return Products.objects.filter(user=self.request.user)


