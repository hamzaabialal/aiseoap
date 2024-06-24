from .models import SignupModel
from rest_framework import serializers


class SignupSerializer(serializers.ModelSerializer):

    """ Serializer for signup functionality"""

    class Meta:
        model = SignupModel
        fields = ['id', 'full_name', "email", "password",
                  "confirm_password", "username"]

    def validate(self, data):
        """validate the password and confirm password"""
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError("Password and confirm password should be same")
        return data

    def validate_emial(self, email):
        """validate the email"""
        if SignupModel.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email already exists")
        return email

    def validate_username(self, username):
        """validate the username"""
        if SignupModel.objects.filter(username=username).exists():
            raise serializers.ValidationError("Username already exists")
        return username

    def create(self, validated_data):
        user = SignupModel.objects.create(
            email=validated_data["email"],
            full_name=validated_data["full_name"],
            username=validated_data["username"],

        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField()




