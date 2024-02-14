# forms.py

from django import forms

class QuerySolutionForm(forms.Form):
    query_solution = forms.CharField(widget=forms.Textarea)
