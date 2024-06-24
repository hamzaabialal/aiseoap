from .models import Products
from rest_framework import serializers

class ProductsSerializer(serializers.ModelSerializer):
    """Serializer for products"""
    class Meta:
        model = Products
        fields = '__all__'