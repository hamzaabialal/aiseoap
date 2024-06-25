from .models import Blogs
from rest_framework import serializers

class BlogsSerializer(serializers.ModelSerializer):
    """Serializer For Blog Model"""
    class Meta:
        model = Blogs
        fields = '__all__'