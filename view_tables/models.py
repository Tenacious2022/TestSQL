from django.db import models

class Customer(models.Model):
    customerNumber = models.IntegerField(primary_key=True)
    customerName = models.CharField(max_length=50)
    contactLastName = models.CharField(max_length=50)
    contactFirstName = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    addressLine1 = models.CharField(max_length=50)
    addressLine2 = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50, null=True, blank=True)
    postalCode = models.CharField(max_length=15, null=True, blank=True)
    country = models.CharField(max_length=50)
    salesRepEmployeeNumber = models.IntegerField(null=True, blank=True)
    creditLimit = models.FloatField()

    class Meta:
        db_table = 'customers'
        unique_together=("customerNumber","customerName","contactLastName")


class OrderDetail(models.Model):
    orderNumber = models.IntegerField()
    productCode = models.CharField(max_length=15)
    quantityOrdered = models.IntegerField()
    priceEach = models.FloatField()
    orderLineNumber = models.SmallIntegerField()
    class Meta:
        unique_together = ('orderNumber', 'productCode')
        db_table = 'orderdetails'

class Payment(models.Model):
    customerNumber = models.IntegerField()
    checkNumber = models.CharField(max_length=50)
    paymentDate = models.DateTimeField()
    amount = models.FloatField()
    class Meta:
        db_table = 'payments'
        unique_together = ('customerNumber', 'checkNumber')
        

class Product(models.Model):
    productCode = models.CharField(max_length=15, primary_key=True)
    productName = models.CharField(max_length=70)
    productLine = models.CharField(max_length=50)
    productScale = models.CharField(max_length=10)
    productVendor = models.CharField(max_length=50)
    productDescription = models.TextField()
    quantityInStock = models.IntegerField()
    buyPrice = models.FloatField()
    MSRP = models.FloatField()
    class Meta:
        db_table = 'products'
        unique_together=("productCode","productName")

class Employee(models.Model):
    employeeNumber = models.IntegerField(primary_key=True)
    lastName = models.CharField(max_length=50)
    firstName = models.CharField(max_length=50)
    extension = models.CharField(max_length=10)
    email = models.EmailField(max_length=100)
    officeCode = models.CharField(max_length=10)
    reportsTo = models.IntegerField(null=True, blank=True)
    jobTitle = models.CharField(max_length=50)
    class Meta:
        db_table = 'employees'
        unique_together=("employeeNumber","lastName","firstName")


class Office(models.Model):
    officeCode = models.CharField(max_length=10, primary_key=True)
    city = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    addressLine1 = models.CharField(max_length=50)
    addressLine2 = models.CharField(max_length=50, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    country = models.CharField(max_length=50)
    postalCode = models.CharField(max_length=50)
    territory = models.CharField(max_length=10)
    class Meta:
        db_table = 'offices'
        unique_together=("officeCode","city")


class Order(models.Model):
    orderNumber = models.IntegerField(primary_key=True)
    orderDate = models.DateTimeField()
    requiredDate = models.DateTimeField()
    shippedDate = models.DateTimeField()
    status = models.CharField(max_length=255)
    comments = models.TextField(null=True, blank=True)
    customerNumber = models.IntegerField()
    class Meta:
        db_table = 'orders'
        unique_together=("orderNumber","orderDate")

class ProductLine(models.Model):
    productLines = models.CharField(max_length=50, primary_key=True)
    textDescription = models.TextField()

    class Meta:
        db_table = 'productlines'
        unique_together=("productLines","textDescription")




