from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from .models import Company, Department, Employee, Customer, Contract
from .serializers import (
    CompanySerializer,
    DepartmentSerializer,
    EmployeeSerializer,
    CustomerSerializer,
    ContractSerializer,
)


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [AllowAny]


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.select_related('company').all()
    serializer_class = DepartmentSerializer
    permission_classes = [AllowAny]


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.select_related('department', 'department__company').all()
    serializer_class = EmployeeSerializer
    permission_classes = [AllowAny]


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [AllowAny]


class ContractViewSet(viewsets.ModelViewSet):
    queryset = Contract.objects.select_related('company', 'customer').all()
    serializer_class = ContractSerializer
    permission_classes = [AllowAny]