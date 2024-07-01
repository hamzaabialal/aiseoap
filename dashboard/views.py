from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from CompitatorAnalysis.models import SerpResult
from shopifyproducts.models import AnalyticsData


# Create your views here.
class DashboardView(TemplateView):
    template_name = 'dashboard/dashboard-2.html'
    authentication_classes= [JWTAuthentication]
    permission_classess = [IsAuthenticated]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            latest_analytics = AnalyticsData.objects.filter(user=self.request.user.id).latest('created_at')
            analytics_data = latest_analytics.data
        except AnalyticsData.DoesNotExist:
            analytics_data = {
                'total_sales': 0,
                'target_sale': 0,
                'total_orders': 0,
                'products_sold': 0,
                'new_customers': 0,
                'repeat_customer_rate': 0,
                'average_order_value': 0,
                'last_week_sale': 0,
                'last_month_sale': 0,
                'top_products': []
            }
        # Calculate progress percentage
        if analytics_data['target_sale'] != 0:
            sales_progress = (analytics_data['total_sales'] / analytics_data['target_sale']) * 100
        else:
            sales_progress = 0
        context['analytics_data'] = analytics_data
        context['sales_progress'] = sales_progress
        return context

class CustomersPageView(TemplateView):
    template_name = 'customers.html'
    authentication_classes= [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = self.request.user  # Use GET to access query parameters
        if data:
            keyword = SerpResult.objects.filter(user=self.request.user.id).last()
            if keyword:
                serp_datas = SerpResult.objects.filter(query__contains= keyword.query,user=self.request.user.id)
                context['serp_data'] = serp_datas
            return context