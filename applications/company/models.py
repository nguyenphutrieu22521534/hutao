from auditlog.registry import auditlog
from django.db import models
from django.contrib.auth.models import User


class Company(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = "Company"
        verbose_name_plural = "Companies"
        db_table = "company"

auditlog.register(Company)

class Department(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="departments")
    name = models.CharField(max_length=120)

    def __str__(self):
        return f"{self.name} ({self.company.name})"

    class Meta:
        ordering = ["name"]
        verbose_name = "Department"
        verbose_name_plural = "Departments"
        db_table = "department"

auditlog.register(Department)

class Employee(models.Model):
    GENDER_CHOICES = [
        ("M", "Male"),
        ("F", "Female"),
        ("O", "Other"),
    ]
    name = models.CharField(max_length=200)
    email = models.EmailField()
    department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name="employees")
    employee_id = models.CharField(max_length=20, unique=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default="O")

    def __str__(self):
        return f"{self.name} ({self.employee_id})"

    class Meta:
        ordering = ["employee_id"]
        verbose_name = "Employee"
        verbose_name_plural = "Employees"
        db_table = "employee"

auditlog.register(Employee)

class Customer(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = "Customer"
        verbose_name_plural = "Customers"
        db_table = "customer"

auditlog.register(Customer)

class Contract(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="contracts")
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="contracts")
    title = models.CharField(max_length=200,verbose_name="Detail")
    value = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return f"{self.title} - {self.company.name}"

    class Meta:
        ordering = ["title"]
        verbose_name = "Contract"
        verbose_name_plural = "Contracts"
        db_table = "contract"

auditlog.register(Contract)
