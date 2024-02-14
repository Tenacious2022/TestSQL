import os
import django

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sqltest.settings")
django.setup()

import json
from faker import Faker
import random
from datetime import datetime, timedelta
from django.utils import timezone
import pytz
from view_tables.models import ProductLine 



fake = Faker()

# Generate customers data
customers_data = []
for i in range(500):
    customer = {
        "customerNumber": 1000 + i,
        "customerName": fake.company(),
        "contactLastName": fake.last_name(),
        "contactFirstName": fake.first_name(),
        "phone": fake.phone_number(),
        "addressLine1": fake.street_address(),
        "addressLine2": fake.secondary_address(),
        "city": fake.city(),
        "state": fake.state(),
        "postalCode": fake.zipcode(),
        "country": fake.country(),
        "salesRepEmployeeNumber": random.choice([None] + list(range(1000, 1099))),
        "creditLimit": random.uniform(10000, 100000)
    }
    customers_data.append(customer)

# Generate orderdetails data
orderdetails_data = []
for i in range(500):
    orderdetail = {
        "orderNumber": 10000-i-4,
        "productCode": fake.random_element(elements=("P1", "P2", "P3", "P4")),
        "quantityOrdered": random.randint(1, 100),
        "priceEach": random.uniform(10, 500),
        "orderLineNumber": 1000-i-2
    }
    orderdetails_data.append(orderdetail)

# Generate payments data
payments_data = []
for i in range(500):
    payment = {
        "customerNumber": fake.random_int(min=1000, max=1099),
        "checkNumber": 10000+(i+5),
        "paymentDate": (datetime.now() - timedelta(days=random.randint(1, 365))).strftime('%Y-%m-%d %H:%M:%S'),
        "amount": random.uniform(10, 1000)
    }
    payments_data.append(payment)

# Generate products data
products_data = []
for i in range(500):
    product = {
        "productCode": f"P{i + 1}",
        "productName": fake.word(),
        "productLine": fake.random_element(elements=("Electronics", "Toys", "Clothing")),
        "productScale": fake.random_element(elements=("1:12", "1:24", "1:32")),
        "productVendor": fake.company(),
        "productDescription": fake.sentence(),
        "quantityInStock": random.randint(10, 1000),
        "buyPrice": random.uniform(10, 200),
        "MSRP": random.uniform(20, 400)
    }
    products_data.append(product)

# Generate employees data
employees_data = []
for i in range(500):
    employee = {
        "employeeNumber": 1000 + i,
        "lastName": fake.last_name(),
        "firstName": fake.first_name(),
        "extension": fake.random_element(elements=("x123", "x456", "x789")),
        "email": fake.email(),
        "officeCode": fake.random_element(elements=("O1", "O2", "O3", "O4")),
        "reportsTo": random.choice([None] + list(range(1000, 1099))),
        "jobTitle": fake.job()
    }
    employees_data.append(employee)

# Generate offices data
offices_data = []
for i in range(500):
    office = {
        "officeCode": f"O{i + 1}",
        "city": fake.city(),
        "phone": fake.phone_number(),
        "addressLine1": fake.street_address(),
        "addressLine2": fake.secondary_address(),
        "state": fake.state(),
        "country": fake.country(),
        "postalCode": fake.zipcode(),
        "territory": fake.random_element(elements=("NA", "EMEA", "APAC"))
    }
    offices_data.append(office)

# Create a list to store the generated data
order_data = []

# Get the current timezone
current_timezone = timezone.now().astimezone(pytz.utc)

# Helper function to generate random datetime within a given range
def random_datetime(start_date, end_date, tz):
    delta = end_date - start_date
    random_seconds = fake.random_int(min=0, max=delta.total_seconds())
    return start_date + timedelta(seconds=random_seconds)

# Generate 500 random records
for _ in range(500):
    order_number = fake.random_int(min=10000, max=99999)
    start_date = current_timezone - timedelta(days=365)  # One year ago from current time
    end_date = current_timezone
    order_date = random_datetime(start_date, end_date, current_timezone)
    required_date = random_datetime(order_date, end_date, current_timezone)
    shipped_date = random_datetime(order_date, required_date, current_timezone)
    status = fake.random_element(elements=('Shipped', 'Processing', 'Cancelled'))
    comments = fake.text() if fake.boolean(chance_of_getting_true=30) else None
    customer_number = fake.random_int(min=100, max=999)

    order_data.append({
        'orderNumber': order_number,
        'orderDate': order_date.strftime('%Y-%m-%d %H:%M:%S'),
        'requiredDate': required_date.strftime('%Y-%m-%d %H:%M:%S'),
        'shippedDate': shipped_date.strftime('%Y-%m-%d %H:%M:%S'),
        'status': status,
        'comments': comments,
        'customerNumber': customer_number
    })

data = [
    {
        'productLines': 'Classic Cars',
        'textDescription': 'Attention car enthusiasts: Make your wildest car ownership dreams come true. Whether you are looking for classic muscle cars, dream sports cars or movie-inspired miniatures, you will find great choices in this category. These replicas feature superb attention to detail and craftsmanship and offer features such as working steering system, opening forward compartment, opening rear trunk with removable spare wheel, 4-wheel independent spring suspension, and so on. The models range in size from 1:10 to 1:24 scale and include numerous limited edition and several out-of-production vehicles. All models include a certificate of authenticity from their manufacturers and come fully assembled and ready for display in the home or office.'
    },
    {
        'productLines': 'Motorcycles',
        'textDescription': 'Our motorcycles are state of the art replicas of classic as well as contemporary motorcycle legends such as Harley Davidson, Ducati and Vespa. Models contain stunning details such as official logos, rotating wheels, working kickstand, front suspension, gear-shift lever, footbrake lever, and drive chain. Materials used include diecast and plastic. The models range in size from 1:10 to 1:50 scale and include numerous limited edition and several out-of-production vehicles. All models come fully assembled and ready for display in the home or office. Most include a certificate of authenticity.'
    },
    {
        'productLines': 'Planes',
        'textDescription': 'Unique, diecast airplane and helicopter replicas suitable for collections, as well as home, office or classroom decorations. Models contain stunning details such as official logos and insignias, rotating jet engines and propellers, retractable wheels, and so on. Most come fully assembled and with a certificate of authenticity from their manufacturers.'
    },
    {
        'productLines': 'Ships',
        'textDescription': 'The perfect holiday or anniversary gift for executives, clients, friends, and family. These handcrafted model ships are unique, stunning works of art that will be treasured for generations! They come fully assembled and ready for display in the home or office. We guarantee the highest quality, and best value.'
    },
    {
        'productLines': 'Trains',
        'textDescription': 'Model trains are a rewarding hobby for enthusiasts of all ages. Whether you''re looking for collectible wooden trains, electric streetcars or locomotives, you''ll find a number of great choices for any budget within this category. The interactive aspect of trains makes toy trains perfect for young children. The wooden train sets are ideal for children under the age of 5.'
    },
    {
        'productLines': 'Trucks and Buses',
        'textDescription': 'The Truck and Bus models are realistic replicas of buses and specialized trucks produced from the early 1920s to present. The models range in size from 1:12 to 1:50 scale and include numerous limited edition and several out-of-production vehicles. Materials used include tin, diecast and plastic. All models include a certificate of authenticity from their manufacturers and are a perfect ornament for the home and office.'
    },
    {
        'productLines': 'Vintage Cars',
        'textDescription': 'Our Vintage Car models realistically portray automobiles produced from the early 1900s through the 1940s. Materials used include Bakelite, diecast, plastic and wood. Most of the replicas are in the 1:18 and 1:24 scale sizes, which provide the optimum in detail and accuracy. Prices range from $30.00 up to $180.00 for some special limited edition replicas. All models include a certificate of authenticity from their manufacturers and come fully assembled and ready for display in the home or office.'
    },
]

# Insert the data into the database
for item in data:
    product_line_instance = ProductLine(**item)
    product_line_instance.save()



# Combine data for all tables into a dictionary
sample_data = {
    "customers": customers_data,
    "orderdetails": orderdetails_data,
    "payments": payments_data,
    "products": products_data,
    "employees": employees_data,
    "offices": offices_data,
    "orders":order_data,
   
}

# Write data to JSON file
with open("sample_data.json", "w") as json_file:
    json.dump(sample_data, json_file, indent=4)


# Insert data into the ProductLine model



