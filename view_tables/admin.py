from django.contrib import admin
from .models import Customer, OrderDetail, Payment, Product, Employee, Office,Order,ProductLine

class CustomersAdmin(admin.ModelAdmin):
    list_display = ('customerNumber', 'customerName', 'contactLastName', 'contactFirstName', 'phone', 'country')
    
class OrderDetailsAdmin(admin.ModelAdmin):
    list_display = ('orderNumber', 'productCode', 'quantityOrdered', 'priceEach', 'orderLineNumber')

class PaymentsAdmin(admin.ModelAdmin):
    list_display = ('customerNumber', 'checkNumber', 'paymentDate', 'amount')

class ProductsAdmin(admin.ModelAdmin):
    list_display = ('productCode', 'productName', 'productLine', 'productScale', 'productVendor', 'quantityInStock', 'buyPrice', 'MSRP')

class EmployeesAdmin(admin.ModelAdmin):
    list_display = ('employeeNumber', 'lastName', 'firstName', 'extension', 'email', 'officeCode', 'reportsTo', 'jobTitle')

class OfficesAdmin(admin.ModelAdmin):
    list_display = ('officeCode', 'city', 'phone', 'addressLine1', 'country', 'territory')

class OrdersAdmin(admin.ModelAdmin):
    list_display = ('orderNumber', 'orderDate', 'requiredDate',"shippedDate", 'status', 'comments', 'customerNumber')

class ProductLineAdmin(admin.ModelAdmin):
    list_display=("productLines","textDescription")


admin.site.register(Customer, CustomersAdmin)
admin.site.register(OrderDetail, OrderDetailsAdmin)
admin.site.register(Payment, PaymentsAdmin)
admin.site.register(Product, ProductsAdmin)
admin.site.register(Employee, EmployeesAdmin)
admin.site.register(Office, OfficesAdmin)
admin.site.register(Order,OrdersAdmin)
admin.site.register(ProductLine,ProductLineAdmin)


