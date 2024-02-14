import os
import django

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sqltest.settings")
django.setup()

import pandas as pd
from django.db import transaction
from assignments.models import BasicSQL, IntermediateSQL, AdvancedSQL



os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sqltest.settings")
django.setup()


excel_file_path = 'QnAExtra.xlsx'
df = pd.read_excel(excel_file_path)

@transaction.atomic
def populate_database(row):
    level = row['Level'].strip().lower()

    if level == 'easy':
        model = BasicSQL
        marks = 2
    elif level == 'medium':
        model = IntermediateSQL
        marks = 3
    elif level == 'advanced':
        model = AdvancedSQL
        marks = 4
    else:
        raise ValueError(f"Invalid level: {level}")

    question = row['Questions']
    answer = row['Solutions']

    existing_records = model.objects.filter(question=question, answer=answer, marks=marks)

    if existing_records.exists():
        # If a record with the same question, answer, and marks exists, do nothing or update
        pass
    else:
        model.objects.create(question=question, answer=answer, marks=marks)

for index, row in df.iterrows():
    populate_database(row)
