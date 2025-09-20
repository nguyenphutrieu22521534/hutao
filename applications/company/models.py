from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

