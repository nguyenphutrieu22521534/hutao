from auditlog.registry import auditlog
from django.db import models
from django.contrib.auth.models import User


class Apartment(models.Model):
    number = models.CharField(max_length=10, unique=True)
    floor = models.PositiveIntegerField()
    status = models.CharField(max_length=20)

    class Meta:
        ordering = ['floor', 'number']
    
    def __str__(self):
        return f"Apartment {self.number} (Floor {self.floor})"

class Resident(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="resident_profile")
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, related_name="residents")
    phone = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['apartment__floor', 'apartment__number']
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.apartment}"

class ElectricityIndicator(models.Model):
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, related_name="electricity_indicators")
    previous_reading = models.PositiveIntegerField()
    current_reading = models.PositiveIntegerField()
    reading_date = models.DateField()

    class Meta:
        ordering = ['-reading_date']
        unique_together = ['apartment', 'reading_date']
    
    def __str__(self):
        return f"Electricity - {self.apartment} - {self.reading_date}"
    
    @property
    def usage(self):
        return self.current_reading - self.previous_reading

class WaterIndicator(models.Model):
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, related_name="water_indicators")
    previous_reading = models.PositiveIntegerField()
    current_reading = models.PositiveIntegerField()
    reading_date = models.DateField()

    class Meta:
        ordering = ['-reading_date']
        unique_together = ['apartment', 'reading_date']
    
    def __str__(self):
        return f"Water - {self.apartment} - {self.reading_date}"
    
    @property
    def usage(self):
        return self.current_reading - self.previous_reading

class Bill(models.Model):
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, related_name="bills")
    bill_type = models.CharField(max_length=20)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    billing_period_end = models.DateField()
    status = models.CharField(max_length=20)

    class Meta:
        ordering = ['-billing_period_end']
    
    def __str__(self):
        return f"Bill - {self.apartment} - {self.billing_period_end}"

auditlog.register(Apartment)
auditlog.register(Resident)
auditlog.register(ElectricityIndicator)
auditlog.register(WaterIndicator)
auditlog.register(Bill)
