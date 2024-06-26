from django.db import models

from core.models import SignupModel


# Create your models here.
class KeywordResearch(models.Model):
    user = models.ForeignKey(SignupModel, on_delete=models.CASCADE, null=True, blank=True)
    compatitor_keywords = models.JSONField()
    gl = models.CharField(max_length=10, default='us')
    Keywords= models.JSONField()