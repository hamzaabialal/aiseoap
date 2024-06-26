from rest_framework import serializers
from .models import KeywordResearch

class KeywordResearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeywordResearch
        fields = '__all__'