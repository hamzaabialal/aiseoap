from django.db import models

from core.models import SignupModel


# Create your models here.
class Blogs(models.Model):
    """Model for blogs"""
    user= models.ForeignKey(SignupModel, on_delete=models.CASCADE, null=True, blank=True)
    blog_title = models.CharField(max_length=100)
    blog_content = models.TextField()
    blog_created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.blog_title