from django.contrib import admin

from . import models

admin.site.register(models.Apartment)
admin.site.register(models.Resident)
admin.site.register(models.ElectricityIndicator)
admin.site.register(models.WaterIndicator)
admin.site.register(models.Bill)
