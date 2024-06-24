import requests
from django.shortcuts import render, get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from Aiseoapp import settings
from management.models import StoreManagement
from shopifyproducts.models import Products, ShopifyAccessToken, AnalyticsData
from shopifyproducts.serializers import ProductsSerializer


# Create your views here.
class FetchProductsFromShopify(APIView):
    """This Api Is Used For Fetching The Products From Shopify."""
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
    """This Api Is Used For Listing The Products."""
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    queryset = Products
    serializer_class =ProductsSerializer

    def get_queryset(self):
        return Products.objects.filter(user=self.request.user)

class ReteriveProduct(generics.RetrieveAPIView):
    """This Api Is Used For Reteriving The Product."""
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    queryset = Products
    serializer_class = ProductsSerializer

    def get_queryset(self):
        return Products.objects.filter(user=self.request.user)


class FetchShopifyAnalytics(APIView):
    def get(self, request):
        try:
            store = get_object_or_404(StoreManagement, user=request.user)
            access_token = get_object_or_404(ShopifyAccessToken, user=request.user).access_token
            shopify_url = f"https://{store.store_name}.myshopify.com/admin/api/2021-07/reports.json"
            headers = {
                "X-Shopify-Access-Token": access_token
            }

            response = requests.get(shopify_url, headers=headers)
            if response.status_code == 200:
                analytics_data = response.json()
                AnalyticsData.objects.create(user=request.user, data=analytics_data)
                return Response({"message": "Analytics data fetched and stored successfully."}, status=200)
            elif response.status_code == 403:
                return Response({"error": "Access forbidden: Check your API permissions."}, status=403)
            else:
                return Response(
                    {"error": f"Failed to fetch analytics data from Shopify. Status code: {response.status_code}"},
                    status=response.status_code)
        except Exception as e:
            return Response({"error": str(e)}, status=400)
