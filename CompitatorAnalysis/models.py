from django.db import models

# Create your models here.
class SerpResult(models.Model):
    keyword = models.CharField(max_length=255)
    display_link = models.CharField(max_length=255)
    rank = models.IntegerField()
