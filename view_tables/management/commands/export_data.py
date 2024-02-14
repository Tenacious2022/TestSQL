import os
from django.core.management.base import BaseCommand
from django.core import serializers
from django.conf import settings
from view_tables.models import customers, employees, offices, orderdetails, payments, products
# Import other model classes if needed
from datetime import datetime

class Command(BaseCommand):
    help = 'Export data from MySQL tables to JSON'

    def handle(self, *args, **options):
        # Define the table names
        model_classes = [customers, employees, offices, orderdetails, payments, products]

        # Initialize data dictionary
        data = {}

        # Fetch data from each model
        for model_class in model_classes:
            model_name = model_class.__name__
            model_data = serializers.serialize('python', model_class.objects.all())
            data[model_name] = model_data

        # Ensure the directory exists
        os.makedirs('sql_files', exist_ok=True)

        # Convert data to JSON format
        json_data = serializers.serialize('json', data, indent=4)

        # Write JSON data to a file
        with open('sql_files/data.json', 'w') as json_file:
            json_file.write(json_data)

        print("Data has been exported to data.json")
