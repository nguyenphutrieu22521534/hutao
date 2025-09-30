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

auditlog.register(Apartment)

class Resident(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, related_name="residents")
    phone = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['apartment__floor', 'apartment__number']

    def __str__(self):
        return f"{self.name} - {self.apartment}"

auditlog.register(Resident)

class IndicatorBase(models.Model):
    previous_reading = models.PositiveIntegerField()
    current_reading = models.PositiveIntegerField()
    reading_date = models.DateField()

    class Meta:
        abstract = True

class ElectricityIndicator(IndicatorBase):
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, related_name="electricity_indicators")

    class Meta:
        ordering = ['-reading_date']
        unique_together = ['apartment', 'reading_date']

    def __str__(self):
        return f"Electricity - {self.apartment} - {self.reading_date}"

    @property
    def usage(self):
        return self.current_reading - self.previous_reading

auditlog.register(ElectricityIndicator)

class WaterIndicator(IndicatorBase):
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, related_name="water_indicators")

    class Meta:
        ordering = ['-reading_date']
        unique_together = ['apartment', 'reading_date']

    def __str__(self):
        return f"Water - {self.apartment} - {self.reading_date}"

    @property
    def usage(self):
        return self.current_reading - self.previous_reading

auditlog.register(WaterIndicator)

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

auditlog.register(Bill)
