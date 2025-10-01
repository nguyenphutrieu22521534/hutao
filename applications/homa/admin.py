from django.contrib import admin
from . import models

def get_all_field_names(model):
    return [field.name for field in model._meta.fields]

class ApartmentAdmin(admin.ModelAdmin):
    list_display = get_all_field_names(models.Apartment)

class ResidentAdmin(admin.ModelAdmin):
    list_display = get_all_field_names(models.Resident)

class ElectricityIndicatorAdmin(admin.ModelAdmin):
    list_display = get_all_field_names(models.ElectricityIndicator) + ["increase_display"]
    def increase_display(self, obj):
        return obj.increase
    increase_display.short_description = "Increase"

class WaterIndicatorAdmin(admin.ModelAdmin):
    list_display = get_all_field_names(models.WaterIndicator) + ["increase_display"]
    def increase_display(self, obj):
        return obj.increase
    increase_display.short_description = "Increase"

class BillAdmin(admin.ModelAdmin):
    list_display = get_all_field_names(models.Bill)

admin.site.register(models.Apartment, ApartmentAdmin)
admin.site.register(models.Resident, ResidentAdmin)
admin.site.register(models.ElectricityIndicator, ElectricityIndicatorAdmin)
admin.site.register(models.WaterIndicator, WaterIndicatorAdmin)
admin.site.register(models.Bill, BillAdmin)
