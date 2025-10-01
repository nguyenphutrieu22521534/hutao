from django.contrib import admin
from . import models

# Helper to get all field names
def get_all_field_names(model):
    return [field.name for field in model._meta.fields]

class CompanyAdmin(admin.ModelAdmin):
    list_display = get_all_field_names(models.Company)

class DepartmentAdmin(admin.ModelAdmin):
    list_display = get_all_field_names(models.Department)

class EmployeeAdmin(admin.ModelAdmin):
    list_display = get_all_field_names(models.Employee)

class CustomerAdmin(admin.ModelAdmin):
    list_display = get_all_field_names(models.Customer)

class ContractAdmin(admin.ModelAdmin):
    list_display = get_all_field_names(models.Contract)

admin.site.register(models.Company, CompanyAdmin)
admin.site.register(models.Department, DepartmentAdmin)
admin.site.register(models.Employee, EmployeeAdmin)
admin.site.register(models.Customer, CustomerAdmin)
admin.site.register(models.Contract, ContractAdmin)
