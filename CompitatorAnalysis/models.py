from django.db import models

class SerpResult(models.Model):
    query = models.JSONField(max_length=255)
    gl = models.CharField(max_length=10, default='us')
    Keywords = models.JSONField()

    def __str__(self):
        return f"SerpResult - Query: {self.query}, GL: {self.gl}"
