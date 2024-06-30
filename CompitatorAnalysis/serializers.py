from rest_framework import serializers
from .models import SerpResult

class SerpDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SerpResult
        fields = ['query', 'gl', 'Keywords', 'user', 'rank', 'search_term', 'link']
