from django.db import models

# Create your models here.

class Company(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    phone = models.CharField(max_length=20)


    def __str__(self):
        return self.name