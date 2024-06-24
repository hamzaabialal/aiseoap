

from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name="login"),
    path('signup/', views.SignupView.as_view(), name="signup"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("login-page/", views.LoginPageView.as_view(), name="login_page"),
]
