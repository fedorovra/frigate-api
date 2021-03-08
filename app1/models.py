from django.db import models

# Create your models here.

class APIKeys(models.Model):
    api_key = models.CharField(max_length=25, unique=True)
    permissions = models.CharField(max_length=250, blank=True, null=True)
    is_active = models.CharField(max_length=1, default='Y', blank=False, null=False)

