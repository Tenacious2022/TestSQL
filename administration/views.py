from django.shortcuts import render, redirect
from django.views import View
from django.shortcuts import reverse
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.db import IntegrityError
from assignments.models import Gradebook
from authentication.views import Authenctication

class Admin:

    """
        This class deals administration functions or tasks
    """

    def display_homepage(self,request):

        """
            render the admin webpage
        """
        return render(request, 'admin_homepage.html')
    def login_as_observer(self,request):
        """
            redirect admin staff from admin page to assignment page
        """
        user = Authenctication.getUsername(request)
        login(request, user)
        return redirect('homepage')
    def add_users(self,request,user_list,role):
        """
            Retrieve the file with list of participants to be added
            add those participants according to the specified role
        """
        if request.method == "POST":
            try:
                file_contents = user_list.read().decode('utf-8')
                lines = file_contents.split('\n')
                for line in lines:
                    data = line.split(" ")
                    if len(data) >= 3:
                        try:
                            username = data[0]
                            email = username + "@myuct.ac.za"
                            print(username)
                            first_name = data[1]
                            last_name = data[2]
                            password = username+"password"
                            if role == 'admin':
                                new_user = User.objects.create_superuser(username=username,
                                                                        email=email,
                                                                        password=password,
                                                                        is_staff = True)
                            elif role == 'student':
                                new_user = User.objects.create_user(username=username,
                                                                    email=email,
                                                                    password=password)
                            else:
                                return HttpResponse('Invalid role')
                            new_user.first_name = first_name
                            new_user.last_name = last_name
                            new_user.save()
                        except IntegrityError:
                            # Handles in case the participant/s in the file already exist
                            messages.error(request, "Participant/s already exist")
                            return redirect('add_users')
            except Exception as e:
                # Handles the case where the file is not found
                messages.error(request, "Invalid file")
                return redirect('user_registration')
            messages.success(request, "Students successfully added")
            return redirect('user_registration')

    def add_user(self,request):
        """
            Retrieve the participant details and their role
            Add partcicipant to their role in the system
        """
        if request.method == "POST":
            username = request.POST['username']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            role = request.POST.get('role')
            if 'file' in request.FILES:
                user_list = request.FILES['file'] # retrieve uploaded file
                self.add_users(request,user_list,role)
            elif username and first_name and last_name:
                try:

                    new_user = None
                    password = username+'password'
                    if role == 'admin':
                        new_user = User.objects.create_superuser(username=username,
                                                                email=email,password=password,
                                                                is_staff = True)
                    elif role == 'student':
                        new_user = User.objects.create_user(username=username,
                                                            email=email,
                                                            password=password)
                    else:
                        return HttpResponse('Invalid role')
                    new_user.first_name = first_name
                    new_user.last_name = last_name
                    new_user.save()
                    messages.success(request, "Successfully added participant")
                    return redirect('user_registration')
                except IntegrityError:
                    messages.error(request, "Participant already exist")
            else:
                messages.error(request, "Please choose atleast one option")
                return redirect('user_registration')
        return render(request, 'user_registration.html')


    def remove_user(self,request,selected_users):
        """
            Retrieve partcipant username
            Remove partcicpant from system
        """
        if request.method == "POST":
            try:
                if selected_users:
                    for user in selected_users:
                        username = user
                        user_to_delete = User.objects.get(username=username)
                        user_to_delete.delete()

                else:
                    messages.error(request, "No participant selected")
            except User.DoesNotExist:
                # Handles the case where entered username does not exist
                # Return a error message
                # Return to admin homepage
                messages.error(request, ("User not found"))
                return redirect('user_list')
        messages.success(request, "Participant/s successfully removed")
        return redirect ('user_list')

    def list_users(self, request):
        """
            Return all partcipants
            Return participant with username matching search query
        """
        users = User.objects.all()
        if request.method == "POST":
            # Handles the select request
            selected_users = request.POST.getlist('selected_users')
            # Handles the search request
            search_query = request.POST.get('search_query', '')
            if selected_users:
                self.remove_user(request,selected_users)
            elif search_query:
                users = users.filter(username__icontains=search_query) # filter users with matching search query
        user_list = users.values('username','first_name','last_name','is_staff')
        return render(request, 'user_list.html', {'users': user_list})
    def resources(self,request):
        """
            Redirect to django admin for more configuration
        """
        admin_url = reverse('admin:index')
        return HttpResponseRedirect(admin_url)
    def edit_grades(self,request):
        """
            Redirect to model GradeBook for grade configuration
        """
        admin_url = reverse('admin:%s_%s_changelist' % (Gradebook._meta.app_label,
                                                         Gradebook._meta.model_name))
        return HttpResponseRedirect(admin_url)
    def view_grades(self,request):
        """
            Return grades for all participants
        """
        students = Gradebook.objects.all()
        try:
            students = Gradebook.objects.all()
        except Gradebook.DoesNotExist:
            # Handle the case where the student's data doesn't exist
            # You might want to return an error message or take some other action
            students = None

        # Check if the student data exists
        if students:
            # Initialize variables to store total marks and counts for each level
            total_easy = 0
            total_intermediate = 0
            total_hard = 0
            count = 0

            # Loop through the queryset to calculate averages
            for student in students:
                total_easy += student.easy
                total_intermediate += student.intermediate
                total_hard += student.hard
                count += 1

            # Calculate averages and round to two decimal places
            easy = round((total_easy / (count * 2)) / 10 * 100, 2)
            intermediate = round((total_intermediate / (count * 2)) / 10 * 100, 2)
            hard = round((total_hard / (count * 2)) / 10 * 100, 2)
        else:
            # Handle the case where the student data doesn't exist
            # You might want to return an error message or take some other action
            easy = 0
            intermediate = 0
            hard = 0
        total = 2*10+3*10+4*10

        # Pass the student data to the template
        return render(request, 'admin_gradebook.html',
                       {'students': students,
                         'easy': easy, 
                         'intermediate': intermediate, 
                         'hard': hard,
                         'total':total})
    