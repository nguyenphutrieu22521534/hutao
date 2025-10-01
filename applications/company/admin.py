from django.contrib import admin
from . import models
from django.contrib.humanize.templatetags.humanize import intcomma
from import_export.admin import ImportExportModelAdmin

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
    search_fields = ["name"]

class ContractAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    def formatted_value(self, obj):
        return intcomma(obj.value)
    formatted_value.short_description = "Value"

    list_display = ['company', 'customer', 'title'] + ["formatted_value"]
    list_filter = ["company", "customer"]
    list_per_page = 10
    

admin.site.register(models.Company, CompanyAdmin)
admin.site.register(models.Department, DepartmentAdmin)
admin.site.register(models.Employee, EmployeeAdmin)
admin.site.register(models.Customer, CustomerAdmin)
admin.site.register(models.Contract, ContractAdmin)
