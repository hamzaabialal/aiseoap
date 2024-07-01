from datetime import datetime, timedelta

from django.utils.timezone import now
from django.views.generic import TemplateView
from rest_framework import status
import requests
from django.shortcuts import render, get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from collections import Counter, defaultdict
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
        base_url = f"https://{store.store_name}.myshopify.com/"
        headers = {
            "X-Shopify-Access-Token": access_token
        }
        response = requests.get(shopify_url, headers=headers)
        if response.status_code == 200:
            products = response.json().get("products", [])
            for product_data in products:
                handle = product_data["handle"]
                product_url = f"{base_url}products/{handle}"
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
                        "img": product_data["images"][0]["src"],
                        "product_url": product_url




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
    def fetch_orders(self, store, access_token, start_date, end_date):
        params = {
            "status": "any",
            "created_at_min": start_date.isoformat() + "T00:00:00Z",
            "created_at_max": end_date.isoformat() + "T23:59:59Z"
        }
        orders_endpoint = f"https://{store.store_name}.myshopify.com/admin/api/2024-01/orders.json"
        headers = {
            "X-Shopify-Access-Token": access_token,
            "Content-Type": "application/json"
        }
        response = requests.get(orders_endpoint, headers=headers, params=params)
        if response.status_code == 200:
            return response.json().get('orders', [])
        return []

    def calculate_total_sales(self, orders):
        return sum(float(order['total_price']) for order in orders)

    def get(self, request, *args, **kwargs):
        store = get_object_or_404(StoreManagement, user=request.user)
        access_token = get_object_or_404(ShopifyAccessToken, user=request.user).access_token

        today = datetime.utcnow()
        start_of_week = today - timedelta(days=today.weekday() + 7)
        end_of_week = start_of_week + timedelta(days=6)

        start_of_last_week = start_of_week - timedelta(days=7)
        end_of_last_week = start_of_week - timedelta(days=1)

        start_of_month = today.replace(day=1)
        end_of_last_month = start_of_month - timedelta(days=1)
        start_of_last_month = end_of_last_month.replace(day=1)

        orders_last_week = self.fetch_orders(store, access_token, start_of_last_week, end_of_last_week)
        orders_last_month = self.fetch_orders(store, access_token, start_of_last_month, end_of_last_month)
        orders_current_month = self.fetch_orders(store, access_token, start_of_month, today)

        last_week_sales = self.calculate_total_sales(orders_last_week)
        last_month_sales = self.calculate_total_sales(orders_last_month)

        orders = self.fetch_orders(store, access_token, start_of_month, today)
        total_sales = self.calculate_total_sales(orders)
        total_orders = len(orders)
        products_sold = sum(sum(int(line_item['quantity']) for line_item in order['line_items']) for order in orders)
        new_customers = sum(1 for order in orders if
                            'customer' in order and order['customer'] and order['customer'].get('orders_count', 0) == 1)
        average_order_value = total_sales / total_orders if total_orders > 0 else 0
        repeat_customers = sum(1 for order in orders if
                               'customer' in order and order['customer'] and order['customer'].get('orders_count',
                                                                                                   0) > 1)
        repeat_customer_rate = repeat_customers / total_orders if total_orders > 0 else 0

        sales_by_country = defaultdict(float)
        for order in orders:
            country = order['shipping_address']['country'] if order.get('shipping_address') else 'Unknown'
            sales_by_country[country] += float(order['total_price'])

        orders_by_month = defaultdict(int)
        for order in orders:
            month = datetime.strptime(order['created_at'], '%Y-%m-%dT%H:%M:%S%z').strftime('%Y-%m')
            orders_by_month[month] += 1

        product_counter = Counter()
        for order in orders:
            for item in order['line_items']:
                product_counter[item['name']] += item['quantity']
        top_products = product_counter.most_common(10)

        top_customer_locations = Counter()
        for order in orders:
            if order.get('customer') and order['customer'].get('default_address'):
                city = order['customer']['default_address']['city']
                top_customer_locations[city] += 1
        top_customer_locations = top_customer_locations.most_common(10)

        # Fetch total products
        products_count_endpoint = f"https://{store.store_name}.myshopify.com/admin/api/2024-01/products/count.json"
        response = requests.get(products_count_endpoint, headers=self.headers)
        product_count = response.json().get('count', 0) if response.status_code == 200 else 0

        # Fetch total customers
        customers_count_endpoint = f"https://{store.store_name}.myshopify.com/admin/api/2024-01/customers/count.json"
        response = requests.get(customers_count_endpoint, headers=self.headers)
        customer_count = response.json().get('count', 0) if response.status_code == 200 else 0

        # Set your target sale amount here
        target_sale = 200000
        countries = []
        countries_data = []
        for country in sales_by_country:
            countries.append(str(country))
            countries_data.append(round(sales_by_country[country], 2))

        analytics_data = {
            "total_sales": total_sales,
            "total_orders": total_orders,
            "products_sold": products_sold,
            "new_customers": new_customers,
            "average_order_value": average_order_value,
            "repeat_customer_rate": repeat_customer_rate,
            "sales_by_country": dict(sales_by_country),
            "orders_by_month": dict(orders_by_month),
            "top_products": top_products,
            "top_customer_locations": top_customer_locations,
            "total_products": product_count,
            "total_customers": customer_count,
            "target_sale": target_sale,
            "last_week_sale": last_week_sales,
            "last_month_sale": last_month_sales,
            "countries": countries,
            "countries_data": countries_data,

        }

        AnalyticsData.objects.create(user=request.user, data=analytics_data)

        return Response({"message": "Analytics data saved successfully"}, status=status.HTTP_200_OK)


class ProductsPageView(TemplateView):
    template_name = 'products/products.html'
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = Products.objects.filter(user=self.request.user)
        context['products'] = products
        return context
