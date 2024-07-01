from django.db import models

from core.models import SignupModel


# Create your models here.

from django.db import models

class Products(models.Model):
    """This model is used to store the products of the user."""
    user = models.ForeignKey(SignupModel, on_delete=models.CASCADE, null=True, blank=True)
    shopify_product_id = models.CharField(max_length=100, unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    inventory_quantity = models.IntegerField()
    vendor = models.CharField(max_length=255, blank=True, null=True)
    product_type = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField()
    handle = models.CharField(max_length=255, blank=True, null=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    published_at = models.DateTimeField(blank=True, null=True)
    template_suffix = models.CharField(max_length=255, blank=True, null=True)
    published_scope = models.CharField(max_length=255, blank=True, null=True)
    tags = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True)
    admin_graphql_api_id = models.CharField(max_length=255, blank=True, null=True)
    variants = models.JSONField(blank=True, null=True)
    product_id = models.CharField(max_length=76, null=True, blank=True)
    img = models.CharField(max_length=1000, blank=True, null=True)
    product_url = models.CharField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return self.title



class ShopifyAccessToken(models.Model):
    """This model is used to store the access token of the user."""
    user = models.ForeignKey(SignupModel, on_delete=models.CASCADE)
    access_token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email

class AnalyticsData(models.Model):
    """This model is used to store the analytics data of the user."""
    user = models.ForeignKey(SignupModel, on_delete=models.CASCADE)
    data = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email

