from django.test import TestCase
from django.urls import reverse

from management.models import StoreManagement


class TestStoreApis(TestCase):
    def setUp(self):
        pass

    def test_store_create(self):
        """Test store create api"""
        data = {
            "store_name": "test",
            "store_address": "test",
            "store_phone": "03047670164",
            "store_email": "test@gmail.com",
            "store_owner": "test"
        }
        response = self.client.post(reverse("store_create"), data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["store_name"], "test")
        self.assertEqual(response.data["store_address"], "test")
        self.assertEqual(response.data["store_phone"], "03047670164")
        self.assertEqual(response.data["store_email"], "test@gmail.com")

    def test_create_invalid_phone(self):
        """Test create store with invalid phone number"""
        data = {
            "store_name": "test",
            "store_address": "test",
            "store_phone": "0304767",
            "store_email": "test@gmail.com",
            "store_owner": "test"
            }
        response = self.client.post(reverse("store_create"), data)
        self.assertEqual(response.status_code, 400)

    def test_create_invalid_phone_digit(self):
        """Test create store with invalid phone number"""
        data = {
            "store_name": "test",
            "store_address": "test",
            "store_phone": "0304767abc",
            "store_email": "test@gmail.com",
            "store_owner": "test"
            }
        response = self.client.post(reverse("store_create"), data)
        self.assertEqual(response.status_code, 400)

    def test_store_with_empty_email(self):
        """Test create store without email"""
        data = {
            "store_name": "test",
            "store_address": "testNow street 4 Dubai",
            "email": "",
            "store_phone": "03047670164",
            "store_owner": "test"
        }
        response = self.client.post(reverse("store_create"), data)
        self.assertEqual(response.status_code, 400)

    def test_store_with_empty_name(self):
        """Test create store without name"""
        data = {
            "store_name": "",
            "store_address": "test",
            "email": "test@gmail.com",
            "store_phone": "03047670164",
            "store_owner": "test"
        }
        response = self.client.post(reverse("store_create"), data)
        self.assertEqual(response.status_code, 400)

    def test_store_with_empty_address(self):
        """Test create store without address"""
        data = {
            "store_name": "test",
            "store_address": "",
            "email": "test@gmail.com",
            "store_phone": "03047670164",
            "store_owner": "test"
            }
        response = self.client.post(reverse("store_create"), data)
        self.assertEqual(response.status_code, 400)

    def test_store_with_empty_owner(self):
        """Test create store without owner"""
        data = {
            "store_name": "test",
            "store_address": "test",
            "email": "test@gmail.com",
            "store_phone": "03047670164",
            "store_owner": ""}
        response = self.client.post(reverse("store_create"), data)
        self.assertEqual(response.status_code, 400)


class TestStoreReteriveView(TestCase):
    def setUp(self):
        self.store = StoreManagement.objects.create(
            store_name="test",
            store_address="test",
            store_phone="03047670164",
            store_email="test@gmail.com",
            store_owner = "Test",
        )
    def test_store_reterive(self):
        """Test store reterive api"""
        response = self.client.get(reverse("store_reterive", kwargs={"pk": self.store.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["store_name"], "test")
        self.assertEqual(response.data["store_address"], "test")
        self.assertEqual(response.data["store_phone"], "03047670164")
        self.assertEqual(response.data["store_email"], "test@gmail.com")
        self.assertEqual(response.data["store_owner"], "Test")
