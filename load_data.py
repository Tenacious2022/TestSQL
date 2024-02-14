import os
import django

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sqltest.settings")
django.setup()


import json
from datetime import datetime
from view_tables.models import Customer, OrderDetail, Payment, Product, Employee, Office,Order
from django.core.exceptions import ObjectDoesNotExist


# Read JSON data from the file
with open('sample_data.json', 'r') as json_file:
    data = json.load(json_file)

# Load Customer data
for customer_data in data['customers']:
    try:
        customer = Customer.objects.get(customerNumber=customer_data['customerNumber'])
    except Customer.DoesNotExist:
        customer = Customer(**customer_data)
    customer.save()

# Load OrderDetail data
for order_detail_data in data['orderdetails']:
    try:
        order_detail = OrderDetail.objects.get(orderNumber=order_detail_data['orderNumber'],
                                                 productCode=order_detail_data['productCode'])
    except OrderDetail.DoesNotExist:
        order_detail = OrderDetail(**order_detail_data)
    order_detail.save()

# Load Payment data
for payment_data in data['payments']:
    try:
        payment = Payment.objects.get(customerNumber=payment_data['customerNumber'],
                                       checkNumber=payment_data['checkNumber'])
    except Payment.DoesNotExist:
        payment = Payment(**payment_data)
        payment.paymentDate = datetime.strptime(payment_data['paymentDate'], '%Y-%m-%d %H:%M:%S')
    payment.save()

# Load Product data
for product_data in data['products']:
    try:
        product = Product.objects.get(productCode=product_data['productCode'])
    except Product.DoesNotExist:
        product = Product(**product_data)
    product.save()

# Load Employee data
for employee_data in data['employees']:
    try:
        employee = Employee.objects.get(employeeNumber=employee_data['employeeNumber'])
    except Employee.DoesNotExist:
        employee = Employee(**employee_data)
    employee.save()

# Load Office data
for office_data in data['offices']:
    try:
        office = Office.objects.get(officeCode=office_data['officeCode'])
    except Office.DoesNotExist:
        office = Office(**office_data)
    office.save()
# Load Order data
for order_data in data['orders']:
    try:
        order_instance = Order.objects.get(orderNumber=order_data['orderNumber'])
    except Order.DoesNotExist:
        order_instance = Order(**order_data)
    order_instance.save()
    