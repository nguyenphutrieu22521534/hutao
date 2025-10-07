from django.db.models import Count, Sum, Avg, Max, F, Q
from datetime import date, timedelta
from applications.company.models import Company, Department, Employee, Customer, Contract
from applications.homa.models import Apartment, Resident, ElectricityIndicator, WaterIndicator, Bill


# Lấy danh sách Employee và kèm thông tin Department + Company (tránh N+1 query)

employees = Employee.objects.select_related('department', 'department__company').all()
for emp in employees:
    print(f"- {emp.name} ({emp.employee_id})")
    print(f"  Department: {emp.department.name}")
    print(f"  Company: {emp.department.company.name}")

# Lấy toàn bộ Department, prefetch danh sách Employee
departments = Department.objects.prefetch_related('employees').all()
for dept in departments:
    emp_count = dept.employees.count()
    print(f"- {dept.name} ({dept.company.name}): {emp_count} employees")
    for emp in dept.employees.all():
        print(f"{emp.name} ({emp.employee_id})")

#Đếm số Employee của mỗi Department, sắp xếp giảm dần
departments_with_count = Department.objects.annotate(
    employee_count=Count('employees')
).order_by('-employee_count')
for dept in departments_with_count:
    print(f"- {dept.name}: {dept.employee_count} employees")

# Tính tổng value của tất cả Contract cho từng Company
companies_with_total = Company.objects.annotate(
    total_contract_value=Sum('contracts__value')
)
for company in companies_with_total:
    total = company.total_contract_value or 0
    print(f"- {company.name}: {total}")

# Tìm Customer có từ 2 hợp đồng trở lên
customers_with_contracts = Customer.objects.annotate(
    contract_count=Count('contracts')
).filter(contract_count__gte=2)
for customer in customers_with_contracts:
    print(f"- {customer.name}: {customer.contract_count} contracts")

# Tính tổng total_amount của Bill chưa thanh toán cho từng Apartment
apartments_with_unpaid = Apartment.objects.annotate(
    unpaid_total=Sum('bills__total_amount', filter=Q(bills__status='unpaid'))
).filter(unpaid_total__isnull=False)
for apt in apartments_with_unpaid:
    print(f"- Apartment {apt.number} (Floor {apt.floor}): {apt.unpaid_total}")

# Tìm Apartment có tổng tiền Bill chưa thanh toán cao nhất
apartment_highest_unpaid = Apartment.objects.annotate(
    unpaid_total=Sum('bills__total_amount', filter=Q(bills__status='unpaid'))
).filter(unpaid_total__isnull=False).order_by('-unpaid_total').first()

if apartment_highest_unpaid:
    print(f"Apartment {apartment_highest_unpaid.number}")
    print(f"Tổng bill chưa thanh toán: {apartment_highest_unpaid.unpaid_total}")
else:
    print("Không có apartment nào có bill chưa thanh toán")

# Với mỗi Company, đếm số Contract hiện có
companies_with_contract_count = Company.objects.annotate(
    contract_count=Count('contracts')
)
for company in companies_with_contract_count:
    print(f"- {company.name}: {company.contract_count} contracts")

# Với mỗi Customer, tính giá trị trung bình của các hợp đồng
customers_with_avg = Customer.objects.annotate(
    avg_contract_value=Avg('contracts__value'),
).filter(contract_count__gt=0)
for customer in customers_with_avg:
    print(f"- {customer.name}: {customer.avg_contract_value}")

# Tìm những Department không có Employee nào
empty_departments = Department.objects.annotate(
    employee_count=Count('employees')
).filter(employee_count=0)
print(f"Tìm thấy {empty_departments.count()} departments:")
for dept in empty_departments:
    print(f"- {dept.name} ({dept.company.name})")

# Lấy Apartment, prefetch cả water_indicators và electricity_indicators
apartments_with_indicators = Apartment.objects.prefetch_related(
    'water_indicators',
    'electricity_indicators'
).all()
for apt in apartments_with_indicators:
    water_count = apt.water_indicators.count()
    elec_count = apt.electricity_indicators.count()
    print(f"- Apartment {apt.number}")
    print(f"Water indicators: {water_count}, Electricity indicators: {elec_count}")

# Tìm Bill gần nhất cho một Apartment cụ thể
apartment_number = "A101"
apartment = Apartment.objects.get(number=apartment_number)
latest_bill = Bill.objects.filter(apartment=apartment).order_by('-billing_period_end').first()
print(f"Apartment: {apartment_number}")
print(f"Bill type: {latest_bill.bill_type}")
print(f"Amount: {latest_bill.total_amount} VND")
print(f"Period end: {latest_bill.billing_period_end}")
print(f"Status: {latest_bill.status}")

# Lấy Company, prefetch sẵn tất cả Contract
companies_with_contracts = Company.objects.prefetch_related('contracts').all()
for company in companies_with_contracts:
    contracts = company.contracts.all()
    total_value = sum(c.value for c in contracts)
    print(f"- {company.name}: {contracts.count()} contracts, Total: {total_value}")

# Đếm số Resident đang hoạt động trên từng floor
floors_with_residents = Apartment.objects.values('floor').annotate(
    active_resident_count=Count('residents', filter=Q(residents__is_active=True))
)
for floor in floors_with_residents:
    print(f"- Floor {floor['floor']}: {floor['active_resident_count']} active residents")

# Tính tổng phần nước tiêu thụ tăng thêm trong khoảng thời gian

# Tính tổng tiền Bill chia theo bill_type cho Apartment cụ thể
apartment_number = "A101"  # Thay bằng số apartment có trong DB
bill_summary = Bill.objects.filter(
    apartment__number=apartment_number
).values('bill_type').annotate(
    total=Sum('total_amount'),
)

print(f"Apartment: {apartment_number}")
for item in bill_summary:
    print(f"- {item['bill_type']}: {item['total']}")

# Lấy Customer có tổng giá trị hợp đồng vượt ngưỡng
threshold = 1000000  # Ngưỡng 1 triệu
high_value_customers = Customer.objects.annotate(
    total_contract_value=Sum('contracts__value')
).filter(total_contract_value__gt=threshold)

print(f"Ngưỡng: {threshold} VND")
for customer in high_value_customers:
    print(f"- {customer.name}: {customer.total_contract_value} VND")


# Tính tổng toàn bộ value hợp đồng của hệ thống

total_system_value = Contract.objects.aggregate(
    total=Sum('value'),
    count=Count('id'),
    avg=Avg('value'),
    max=Max('value')
)
print(f"Tổng giá trị tất cả hợp đồng: {total_system_value['total']} VND")
print(f"Số lượng hợp đồng: {total_system_value['count']}")
print(f"Giá trị trung bình: {total_system_value['avg']} VND")
print(f"Hợp đồng lớn nhất: {total_system_value['max']} VND")