from .models import StoreManagement
from rest_framework import serializers


class StoreManagementSerializer(serializers.ModelSerializer):
    """Serializer for store management"""
    class Meta:

        model = StoreManagement
        fields = '__all__'

    def validate(self ,data):
        """validate the phone number"""
        if len(data["store_phone"]) <= 10:
            raise serializers.ValidationError("Phone number should be 10 digits")
        elif data["store_phone"].isdigit() == False:
            raise serializers.ValidationError("Phone number should be in digits")
        return data
    def create(self, validated_data):
        return StoreManagement.objects.create(**validated_data)
