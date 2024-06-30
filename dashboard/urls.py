
from . import  views
from django.urls import path, include

urlpatterns = [
    path('dashboard/', views.DashboardView.as_view(), name="dashboard"),
    path('customers/', views.CustomersPageView.as_view(), name='customers')
]
