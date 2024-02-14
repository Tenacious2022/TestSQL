"""sqltest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from assignments import views as assignment
from django.conf import settings
from django.conf.urls.static import static
from practiceAssignments.views import PracticeAssignment
from authentication.views import Authenctication
from administration.views import Admin
from assignments.views import Assignment

from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)

urlpatterns = [
    path('admin/', admin.site.urls,name='admin'),


    #-----------------------  Assignment URLS ---------------------------------------------
 
    path('attemptAssignment/', Assignment().displayQuestions, name='attemptAssignment'),
    path('submit_answer/', Assignment().submitAnswer, name='submit_answer'),
    path('gradebook/',Assignment().gradebook,name = 'gradebook'),
    path('assignmentSetup/',Assignment().assignmentSetup,name='assignmentSetup'),
    path('assignmentConfig/', Assignment().assignmentConfig, name='assignmentConfig'),

    #------------------------------Auth URLS -------------------------


    #homepage
    path('',Authenctication().login_user,name = 'login'),
    path('homepage/', Authenctication().homepage, name='homepage'),


        #Administration
    path('admin_homepage/',Admin().display_homepage,name='admin_homepage'),
    path('add_users/',Admin().add_users,name='add_users'),
    path('user_registration/',Admin().add_user,name='user_registration'),
    path('user_removal/',Admin().remove_user,name='user_removal'),
    path('user_list/',Admin().list_users,name='user_list'),
    path('view_grades/',Admin().view_grades,name='view_grades'),
    path('observer_login/',Admin().login_as_observer,name='observer_login'),
    path('resources/',Admin().resources,name='resources'),
    path('edit_grades/',Admin().edit_grades,name='edit_grades'),
     
      #reset password
    path('reset_password/', Authenctication().reset_password, name='reset_password'),
    path('reset_password/', PasswordResetView.as_view(), name='password_reset'),
    path('reset_password/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset_password/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password/complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('forgotPassword/',Authenctication().forgotPassword,name='forgotPassword'),

    

    # ------------------ practice  Asignment ---------------------------------------
    path('select_questions/',PracticeAssignment().select_questions, name='select_questions'),
    path('displayQuestions/', PracticeAssignment().displayQuestions, name='displayQuestions'),
    path('getDatabaseSize/', PracticeAssignment().getDatabaseSize, name='getDatabaseSize'),
    path('submitFeedback/',PracticeAssignment().submit_feedback,name='submit_feedback'),
    path('displayQuestions/', PracticeAssignment().displayQuestions, name='displayQuestions'),  
 

  


] +static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
