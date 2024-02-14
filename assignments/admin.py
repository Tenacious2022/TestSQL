from django.contrib import admin
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import BasicSQL, IntermediateSQL, AdvancedSQL,GeneratedAssignment,SubmitAssignment,Gradebook,AssignmentSettings


class BasicAdmin(admin.ModelAdmin):
    list_display = ('id', 'question')

class IntermediateAdmin(admin.ModelAdmin):
    list_display = ('id', 'question')

class AdvancedAdmin(admin.ModelAdmin):
    list_display = ('id', 'question')

class GeneratedAssignmentAdmin(admin.ModelAdmin):
    list_display = ('id','question','answer','level')

class AssignmentSettingsAdmin(admin.ModelAdmin):
    list_display = ("numAttempts","numQuestions","dueDate")

class SubmitAssignmentAdmin(admin.ModelAdmin):
    list_display=("id","question",'level',"expectedQuery","userQuery","mark","status")

class GradebookAdmin(admin.ModelAdmin):
    list_display = ( "id","studentNum","easy","intermediate","hard","numTemps","overallMarks")


admin.site.register(Gradebook,GradebookAdmin)
admin.site.register(SubmitAssignment,SubmitAssignmentAdmin)
admin.site.register(BasicSQL, BasicAdmin)
admin.site.register(IntermediateSQL, IntermediateAdmin)
admin.site.register(AdvancedSQL, AdvancedAdmin)
admin.site.register(GeneratedAssignment,GeneratedAssignmentAdmin)
admin.site.register(AssignmentSettings,AssignmentSettingsAdmin)


