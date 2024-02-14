from django import forms
from .models import AssignmentSettings

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = AssignmentSettings
        fields = ['numAttempts', 'numQuestions', 'dueDate']