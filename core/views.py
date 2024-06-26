from django.contrib.auth import authenticate
from django.views.generic import TemplateView
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import SignupModel
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import SignupSerializer, LoginSerializer
# Create your views here.


class SignupView(generics.CreateAPIView):
    """View for signup functionality"""
    serializer_class = SignupSerializer
    queryset = SignupModel

    def post(self, request, *args, **kwargs):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                {"message": "User created successfully"}, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(generics.CreateAPIView):
    serializer_class = LoginSerializer

    def create(self, request, *args, **kwargs):
        # Extract email and password from request data
        email = request.data.get("email")
        password = request.data.get("password")

        # Authenticate user with provided credentials
        user = authenticate(email=email, password=password)

        if user is not None:
            # Generate tokens if authentication succeeds
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            # Return tokens in the response
            return Response({
                "access_token": access_token,
                "refresh_token": refresh_token,
            }, status=status.HTTP_200_OK)

        # Return error message if authentication fails
        return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

class LoginPageView(TemplateView):
    template_name = "auth/login-2.html"

class SignupPageView(TemplateView):
    template_name = "auth/register-2.html"
