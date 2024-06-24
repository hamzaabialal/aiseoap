import json
import os

from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from Aiseoapp.settings import BASE_DIR
from core.models import SignupModel


class TestSignupApis(TestCase):
    def setUp(self):
        pass
    def test_signup(self):
        """Test The Signup API"""
        data = {
            "email": "test@gmail.com",
            "username": "test",
            "password": "test123",
            "confirm_password": "test123",
            "full_name": "test"
        }
        response = self.client.post(reverse("signup"), data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["message"], "User created successfully")

    def test_signup_without_full_name(self):
        """Test the Signup API When Full_name Field is Empty"""
        data = {
            "email": "test@gmail.com",
            "username": "test",
            "password": "test123",
            "confirm_password": "test123",
            "full_name": ""
        }
        response = self.client.post(reverse("signup"), data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["message"], "User created successfully")

    def test_signup_without_empty_username(self):
        data = {
            "email": "test@gmail.com",
            "username": "",
            "password": "test123",
            "confirm_password": "test123",
            "full_name": "test"
        }
        response = self.client.post(reverse("signup"), data)
        self.assertEqual(response.status_code, 400)

    def test_signup_without_empty_email(self):
        """Test Signup APi When Email Field is empty In payload"""
        data = {
            "email": "",
            "username": "test",
            "password": "test123",
            "confirm_password": "test123",
            "full_name": "test"
        }
        response = self.client.post(reverse("signup"), data)
        self.assertEqual(response.status_code, 400)

    def test_signup_when_password_are_not_match(self):
        """Test Signup APi When Password and confirm password Are Not Match"""
        data = {
            "email": "test@gmail.com",
            "username": "test",
            "password": "test123",
            "confirm_password": "test12356",
            "full_name": "test"
        }
        response = self.client.post(reverse("signup"), data)
        self.assertEqual(response.status_code, 400)

    def test_signup_when_email_exists(self):
        """Test Signup when user with same Email Already Exists it Returns 400"""
        data = {
            "email": "test@gmail.com",
            "username": "test",
            "password": "test123",
            "confirm_password": "test123",
            "full_name": "test"
        }
        response = self.client.post(reverse("signup"), data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["message"], "User created successfully")
        data1 = {
            "email": "test@gmail.com",
            "username": "test1",
            "password": "test1234",
            "confirm_password": "test1234",
            "full_name": "test1"
        }
        response = self.client.post(reverse("signup"), data1)
        self.assertEqual(response.status_code, 400)

    def test_signup_when_username_exists(self):
        """Test Signup when user with same usename Already Exists it Returns 400"""
        data = {
            "email": "test@gmail.com",
            "username": "test",
            "password": "test123",
            "confirm_password": "test123",
            "full_name": "test"
        }
        response = self.client.post(reverse("signup"), data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["message"], "User created successfully")
        data1 = {
            "email": "test1@gmail.com",
            "username": "test",
            "password": "test1234",
            "confirm_password": "test1234",
            "full_name": "test1"
        }
        response = self.client.post(reverse("signup"), data1)
        self.assertEqual(response.status_code, 400)

    def test_signup_when_fullname_exists(self):
        """Test Signup when user with same fullname Already Exists it Returns 200"""
        data = {
            "email": "test@gmail.com",
            "username": "test",
            "password": "test123",
            "confirm_password": "test123",
            "full_name": "test"
        }
        response = self.client.post(reverse("signup"), data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["message"], "User created successfully")
        data1 = {
            "email": "test1@gmail.com",
            "username": "test1",
            "password": "test1234",
            "confirm_password": "test1234",
            "full_name": "test"
        }
        response = self.client.post(reverse("signup"), data1)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["message"], "User created successfully")

    def test_signup_user_folder_structure(self):
        """Test that when user register his account then its folder structure is created or not"""

        data = {
            "email": "test@gmail.com",
            "username": "test",
            "password": "test123",
            "confirm_password": "test123",
            "full_name": "test"
        }
        response = self.client.post(reverse("signup"), data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["message"], "User created successfully")


        user = SignupModel.objects.filter(email=data["email"])
        user_folder = os.path.join(BASE_DIR, "user_data", user[0].username)
        json_file_path = os.path.join(user_folder, "user_data.json")
        self.assertTrue(os.path.exists(user_folder))
        self.assertTrue(os.path.exists(json_file_path))
        with open(json_file_path, "r") as f:
            saved_user_data = json.load(f)
        self.assertEqual(saved_user_data["email"], data["email"])
        self.assertEqual(saved_user_data["username"],data["username"])
        self.assertEqual(saved_user_data["full_name"], data["full_name"])

class LoginAndLogoutTestCases(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.login_url = reverse('login')
        self.user = get_user_model().objects.create_user(
            email='testuser@example.com',
            username='testuser',
            password='testpassword'
        )
        self.logout_url = reverse('logout')
        self.refresh_token = RefreshToken.for_user(self.user)


    def test_successful_login(self):
        """Test The Login Api With Correct username and password"""

        data = {
            'email': 'testuser@example.com',
            'password': 'testpassword'
        }

        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', response.data)
        self.assertIn('refresh_token', response.data)

    def test_login_with_invalid_credential(self):
        """test the login api with in valid credential"""
        data = {
            "email": "testuser1@gmail.com",
            "password": "testpassword"
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data['message'], 'Invalid credentials')

    def test_successful_logout(self):
        """Test The Logout API By Blocking the refresh token"""

        data = {
            'refresh_token': str(self.refresh_token)
        }

        response = self.client.post(self.logout_url, data, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], 'Logout successful')

    def test_invalid_token(self):
        """test The Logout APi With The Invalid Refresh token in payload"""

        data = {
            'refresh_token': 'invalid_token'
        }

        response = self.client.post(self.logout_url, data, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Invalid token')




