

from django.urls import path
from . import views

urlpatterns = [
    path('details/', views.StoreManagementViews.as_view(), name="store_create"),
    path('details/<int:pk>/', views.StoreManagementReterive.as_view(), name='store_reterive'),
    path('store_manage/', views.StoreManagementTemplate.as_view(), name='store_manage')
   ]
