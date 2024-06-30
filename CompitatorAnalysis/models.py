from django.db import models

class SerpResult(models.Model):
    user = models.ForeignKey('core.SignupModel', on_delete=models.CASCADE, null=True, blank=True)
    query = models.CharField(max_length=255, default='')
    gl = models.CharField(max_length=10, default='us')
    Keywords = models.CharField(max_length=10000, default='')
    rank = models.IntegerField(default=0)
    search_term = models.CharField(max_length=10000, default='')
    link = models.CharField(max_length=10000, default='')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return f"SerpResult - Query: {self.query}, GL: {self.gl}"

