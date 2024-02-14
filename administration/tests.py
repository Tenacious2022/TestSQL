from django.test import TestCase

# Create your tests here.

import csv
from django.contrib.auth.models import User, Group

# def create_student_users_from_file(file_path):
#     try:
#         # Get the 'student' group or create it if it doesn't exist
#         student_group, created = Group.objects.get_or_create(name='student')

#         with open(file_path, 'r') as file:
#             reader = csv.DictReader(file)
#             for row in reader:
#                 first_name = row['first_name']
#                 last_name = row['last_name']
#                 username = row['username']
#                 email = row['email']

#                 # Create a new User object
#                 user = User.objects.create_user(
#                     username=username,
#                     password=None,  # You can set a default password here if needed
#                     first_name=first_name,
#                     last_name=last_name,
#                     email=email,
#                 )

#                 # Add the user to the 'student' group
#                 user.groups.add(student_group)

#                 # Mark the user as active
#                 user.is_active = True
#                 user.save()

#         return True  # Indicates success
#     except Exception as e:
#         return str(e)  # Return the error message if an exception occurs

