from django.db import models
from django.utils import timezone
from datetime import timedelta


#Assignment databases
class BasicSQL(models.Model):

    question = models.TextField()
    answer = models.TextField()
    marks = models.IntegerField(default=2)

    class Meta:
        verbose_name = "Basic Questions"  
        verbose_name_plural = "Basic Questions"
        unique_together = ('question', 'answer','marks')

        

class IntermediateSQL(models.Model):

    question = models.TextField()
    answer = models.TextField()
    marks = models.IntegerField(default=3)


    class Meta:
        verbose_name = "Intermediate Questions"  
        verbose_name_plural = "Intermediate Questions"
        unique_together = ('question', 'answer','marks')

class AdvancedSQL(models.Model):

    question = models.TextField()
    answer = models.TextField()
    marks = models.IntegerField(default=4)

    class Meta:
        verbose_name = "Advanced Questions"  
        verbose_name_plural = "Advanced Questions"
        unique_together = ('question', 'answer','marks')

#generated Assignment
class GeneratedAssignment(models.Model):
    question = models.TextField()
    answer = models.TextField()
    marks = models.PositiveIntegerField()
    level = models.CharField(max_length=20)

class SubmitAssignment(models.Model):
    studentNum = models.TextField()
    question = models.TextField()
    level  = models.TextField()
    expectedQuery = models.JSONField()
    userQuery = models.JSONField()
    mark = models.PositiveIntegerField()
    status = models.TextField()

    def __str__(self):
        return f"Dictionary Model {self.pk}"
    class Meta:
        verbose_name = "Submtted Assignment"  
        verbose_name_plural = "Submtted Assignment"
        unique_together = ('question','level', 'expectedQuery','userQuery',"mark","status")

class Gradebook(models.Model):

    studentNum = models.TextField()
    easy = models.IntegerField(default=0)
    intermediate = models.IntegerField(default=0)
    hard = models.IntegerField(default=0)
    numTemps = models.IntegerField(default=0)
    overallMarks = models.IntegerField(default=0)
    def __str__(self):
        return f"Gradebook (ID: {self.id})"

    class Meta:
        verbose_name = "Gradebook"  
        verbose_name_plural = "Gradebook"

class AssignmentSettings(models.Model):
    numAttempts = models.PositiveIntegerField(default=15)
    numQuestions = models.PositiveIntegerField(default=10)

    # Calculate the default dueDate as today's date plus 14 days
    default_due_date = timezone.now()  + timedelta(days=14)
    dueDate = models.DateTimeField(default=default_due_date)
    def __str__(self):

        return f"Assignment Settings (ID: {self.id})"




        