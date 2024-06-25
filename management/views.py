from django.shortcuts import render
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.views.generic import TemplateView
from .models import StoreManagement
from .serializers import StoreManagementSerializer
from rest_framework import generics
# Create your views here.


class StoreManagementViews(generics.CreateAPIView):
    """View for store management"""
    queryset = StoreManagement
    serializer_class = StoreManagementSerializer
    authentication_classes = [JWTAuthentication]

class StoreManagementReterive(generics.RetrieveAPIView):

    """View for store management list"""
    queryset = StoreManagement.objects.all()
    serializer_class = StoreManagementSerializer
    authentication_classes = [JWTAuthentication]

class StoreManagementTemplate(TemplateView):
    template_name = "store.html"

