from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Company(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Department(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="departments")
    name = models.CharField(max_length=120)

    def __str__(self):
        return f"{self.name} ({self.company.name})"
# Các options on_delete:
    # - CASCADE: Xóa department khi company bị xóa
    # - PROTECT: Ngăn xóa company nếu có department
    # - SET_NULL: Set company_id = NULL
    # - SET_DEFAULT: Set company_id = giá trị mặc định

class Skill(models.Model):
    name = models.CharField(max_length=80)

    def __str__(self):
        return self.name

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="employee_profile")
    department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name="employees")
    skills = models.ManyToManyField(Skill, related_name="employees")

