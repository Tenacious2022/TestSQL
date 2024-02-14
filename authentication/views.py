from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
import os
from django.contrib.auth.models import User
from assignments.models import AssignmentSettings
from sqltest import settings
import secrets
import string
from django.core.mail import send_mail


class Authenctication:


    """
    this class authenicates the user and create user sessions
    """


    def homepage(self,request):

        assgnconf = AssignmentSettings.objects.last()
        date = assgnconf.dueDate

        """
            render student home page
        """
        return render(request, 'homepage.html',{'deadline':date})


    def login_user(self, request):

        """
            creates a log in session for the user and takes them to home page
        
        """
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Store the username in the session
                request.session['username'] = username

                if user.is_superuser:
                    return redirect('admin_homepage')
                else:
                    return redirect('homepage')
            else:
                messages.error(request, "Incorrect email or password, try again")
                return redirect('login')
        else:
            return render(request, 'login_page.html')


    def forgotPassword(self,request):

        """
            takes the name of the username resetting the password and 
            generates verification code that is sent to the user
            username is used to get user email address
        """
        if request.method == "POST":
            try:
                username = request.POST['username']
                user =  User.objects.get(username=username)
                username = user.email
                
                # Generate a random verification code
                verification_code = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(8))

                request.session['verification_code'] = verification_code
                request.session['username'] = username


                # Send an email to the user
                subject = 'Password Reset Verification Code'
                message = "Hi there,\n\nWe heard that you are trying to reset your password, Please confirm that it's really you by entering code below.\nVerification code: "+str(verification_code)+"\n\nRegards,\nSQL-Test Team"
                from_email = 'vutiviindzhaka@outlook.com'
                recipient_list = [username]
                send_mail(subject, message, from_email, recipient_list, fail_silently=False)
                redirect('reset_password')
                return redirect('reset_password')

            except User.DoesNotExist:
                messages.error(request, "User not found")
                return redirect('forgotPassword')
        else:
            # Handle GET request logic (e.g., display the form)
            return render(request, 'forgotPassword.html')
        
    def reset_password(self, request):

        """
            allows the user to reset their pass with a verification code
        """

         #get data from the session
        verification_code = request.session.get('verification_code')
        username = request.session.get('username')
        email=username

        if request.method == "POST":

           

            #data passed by the user
            verificationCode=request.POST['verificationCode']
            new_password = request.POST['new_password']
            confirm_password = request.POST['confirm_password']
            

            if verificationCode == verification_code:
                try:
                    user = User.objects.get(email=email)
                    if new_password == confirm_password:
                        user.set_password(new_password)
                        user.save()
                        messages.success(request, "Password changed successfully")
                        return redirect('login')
                    else:
                        messages.error(request, "Passwords do not match")
                except User.DoesNotExist:
                    messages.error(request, "User not found")
            else:
                messages.error(request, "Invalid verification code")
        
        return render(request, 'resetPassword.html',{'email':email})
   
    def getUsername(self,request):
        """
            get a username from the session
        """
        return request.session.get('username', None)

   
