import json
import os

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

from Aiseoapp.settings import BASE_DIR


# Create your models here.


class SignupModel(AbstractUser):

    """Model for signyp functionality"""

    email = models.EmailField(max_length=100, unique=True)
    full_name = models.CharField(max_length=100, blank=True, null=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=100)
    confirm_password=models.CharField(max_length=100)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return f"{self.email}"

@receiver(post_save, sender=SignupModel)
def create_user_folder(sender, instance, created, **kwargs):
    if created:
        user_folder = os.path.join(BASE_DIR, "user_data", instance.username)
        os.makedirs(user_folder, exist_ok=True)
        user_data ={
            "email": instance.email,
            "full_name": instance.full_name,
            "username": instance.username,
            "created_at": instance.date_joined.strftime("%Y-%m-%d %H:%M:%S"),
        }
        json_file_path =os.path.join(user_folder, "user_data.json")
        with open(json_file_path, "w") as f:
            json.dump(user_data, f, indent=4)
        print("File is Converted Into JSON And Successfully Created")






