import os

# Set the Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sqltest.settings")
import django
django.setup()

from django.db.models import Count
from assignments.models import BasicSQL,IntermediateSQL,AdvancedSQL

# Get a list of question and answer pairs that have duplicates
duplicate_pairs = BasicSQL.objects.values('question', 'answer').annotate(duplicate_count=Count('id')).filter(duplicate_count__gt=1)

for pair in duplicate_pairs:
    duplicates = BasicSQL.objects.filter(question=pair['question'], answer=pair['answer'])
    # Keep the first record (you can change this logic if needed)
    record_to_keep = duplicates.first()
    duplicates.exclude(pk=record_to_keep.pk).delete()

# Get a list of question and answer pairs that have duplicates
duplicate_pairs = IntermediateSQL.objects.values('question', 'answer').annotate(duplicate_count=Count('id')).filter(duplicate_count__gt=1)

for pair in duplicate_pairs:
    duplicates = IntermediateSQL.objects.filter(question=pair['question'], answer=pair['answer'])
    # Keep the first record (you can change this logic if needed)
    record_to_keep = duplicates.first()
    duplicates.exclude(pk=record_to_keep.pk).delete()


# Get a list of question and answer pairs that have duplicates
duplicate_pairs = AdvancedSQL.objects.values('question', 'answer').annotate(duplicate_count=Count('id')).filter(duplicate_count__gt=1)

for pair in duplicate_pairs:
    duplicates = AdvancedSQL.objects.filter(question=pair['question'], answer=pair['answer'])
    # Keep the first record (you can change this logic if needed)
    record_to_keep = duplicates.first()
    duplicates.exclude(pk=record_to_keep.pk).delete()
