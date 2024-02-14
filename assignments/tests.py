import os
import django
from django.test import TestCase
from assignments.models import BasicSQL, IntermediateSQL, AdvancedSQL
from practiceAssignments.models import Question

from .views import generateAssignment

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sqltest.settings")
django.setup()

class testSize(TestCase):

    def test_generateQuestions(self):
        basic_size = BasicSQL.objects.count()
        intermediate_size = IntermediateSQL.objects.count()
        advanced_size = AdvancedSQL.objects.count()
        print(basic_size)
        q = Question.objects.all()

        for i in q:
            print(i)
        print(f"Intermediate SQL questions: {intermediate_size}")
        print(f"Advanced SQL questions: {advanced_size}")
    
    def dict():
        print(generateAssignment)

if __name__ == '__main__':
    dict()
