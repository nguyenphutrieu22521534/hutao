from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    CompanyViewSet,
    DepartmentViewSet,
    EmployeeViewSet,
    CustomerViewSet,
    ContractViewSet,
)

router = DefaultRouter()
router.register(r'companies', CompanyViewSet, basename='company')
router.register(r'departments', DepartmentViewSet, basename='department')
router.register(r'employees', EmployeeViewSet, basename='employee')
router.register(r'customers', CustomerViewSet, basename='customer')
router.register(r'contracts', ContractViewSet, basename='contract')

urlpatterns = [
    path('', include(router.urls)),
]