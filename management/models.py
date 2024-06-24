from django.db import models

from core.models import SignupModel


# Create your models here.

class StoreManagement(models.Model):
    """Model for store management"""
    user = models.ForeignKey(SignupModel, on_delete=models.CASCADE, null=True, blank=True)
    store_name = models.CharField(max_length=100)
    store_address = models.TextField()
    store_phone = models.CharField(max_length=15)
    store_email = models.EmailField(max_length=100)
    store_owner = models.CharField(max_length=100)
    store_created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.store_name