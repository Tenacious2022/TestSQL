from django.contrib import messages
from django.shortcuts import redirect, render
from assignments.models import BasicSQL, IntermediateSQL, AdvancedSQL,GeneratedAssignment,SubmitAssignment,Gradebook,AssignmentSettings
import random
from django.db import IntegrityError, connection
from authentication.views import Authenctication
from .AdminForm import AssignmentForm

class Assignment:
    def  assignmentSetup(self,request):
        """
            render the Assignment configuration for the admin
        """
        maxSize = min(BasicSQL.objects.count(),IntermediateSQL.objects.count(),AdvancedSQL.objects.count())
        return render(request,'assignmentSetup.html',{"maxSize":maxSize})

    def randomiseQuestions(self,numQuestions):

        if numQuestions is None or numQuestions==0:
            numQuestions=10
        else:
            numQuestions = numQuestions

        """
        Generate random pks for different levels (basic, intermediate, advanced) and store them in lists.

        Returns:
            dict: A dictionary containing lists of random question IDs for each level.
        """

        # Lists of different levels to store PKs
        basicQuestions = []
        intermediateQuestions = []  # Corrected the key to "intermediateQuestions"
        advancedQuestions = []
        
        # Define lists in a dictionary
        levels = {
            "basicQuestions": basicQuestions,
            "intermediateQuestions": intermediateQuestions,  # Corrected the key
            "advancedQuestions": advancedQuestions
        }

        for levelName, level in levels.items(): 
            
            # Used to check if an ID has been used already
            usedId = []
            # Calculate the size of the level database
            modelName = (levelName[:-9].capitalize()) + "SQL"
            size = getattr(globals()[modelName], "objects").count()

            while len(level) != numQuestions:
                
                index = random.randint(1, size)
                if index not in usedId:
                    usedId.append(index)
                    level.append(index)

        # Returns random IDs of records
        return levels


    def generateAssignment(self):

        """
            Generate questions using random pks generated above for different levels (basic, intermediate, advanced) and store them in lists.

            Returns:
                dict: A dictionary containing lists of random questions,answers,marks for each level.
        """
        # Generate levels

        assignment = AssignmentSettings.objects.last()
        numQuestions = int(assignment.numQuestions)
        print('number of questions',numQuestions)
        levels = Assignment().randomiseQuestions(numQuestions)

        # Prepare a dictionary with questions for each level
        questions = {
            'Basic': levels['basicQuestions'],
            'Intermediate': levels['intermediateQuestions'],
            'Advanced': levels['advancedQuestions'],
        }

        # Iterate through each level and its questions
        index =1
        for level, levelItems in questions.items():
            
            for i in levelItems:
                # Create a model for each database table
                questionObj=''
                if level=='Basic':
                    questionObj=BasicSQL.objects.get(pk=i)
                elif level=='Intermediate':
                    questionObj=IntermediateSQL.objects.get(pk=i)
                elif level=='Advanced':
                    questionObj=AdvancedSQL.objects.get(pk=i)
                
                question = questionObj.question
                solution = questionObj.answer
                marks = questionObj.marks

                # store the generated questions in a temporal database
                assignment = GeneratedAssignment(id=index,
                    question=question,
                    answer=solution,
                    marks=marks,
                    level=level
                )
                assignment.save()
                index+=1
        if index==3*numQuestions:
            pass



    from django.db import IntegrityError  # Import IntegrityError for database errors

    def displayQuestions(self,request):
        try:
            # Delete all records in the SubmitAssignment model
            SubmitAssignment.objects.all().delete()
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM sqlite_sequence WHERE name = 'SubmitAssignment'")
        except:
            return render(request, 'homepage.html')

        try:
            # Handle the number of attempts by the user
            username = Authenctication().getUsername(request)
            if not Gradebook.objects.filter(studentNum=username).exists():
                # If it's empty, create a new instance with numTemps set to 1
                gradebook = Gradebook(numTemps=1, studentNum=username)
                gradebook.save()

            # Retrieve the first Gradebook instance for the specific student
            gradebook = Gradebook.objects.get(studentNum=username)

            # Check if the number of attempts made by a user is less than the maximum allowed attempts
            assignment_settings = AssignmentSettings.objects.last()

            if gradebook.numTemps < assignment_settings.numAttempts:

                # Increment the numTemps
                temps = gradebook.numTemps + 1
                gradebook.numTemps = temps
                gradebook.save()

                # Check if a GeneratedAssignment exists, and if not, generate one
                if not GeneratedAssignment.objects.exists():
                    Assignment().generateAssignment()

                # Retrieve assignment data from the GeneratedAssignment model
                assignment_data = GeneratedAssignment.objects.all()
            else:
                return render(request, 'homepage.html', {"message": 'Maximum number of attempts have been reached.'})

        except IntegrityError as e:
            # Handle IntegrityError, which can occur if the database encounters an issue
            return render(request, 'homepage.html', {"message": 'An error occurred while generating the assignment.', "error": str(e)})
        
        assgnconf = AssignmentSettings.objects.last()
        date = assgnconf.dueDate
        hours = 3
        remaining_time = hours*60*60
        return render(request, 'displayQuestions.html', {'questions_data': assignment_data, 'user': username,'remaining_time': remaining_time, 'deadline': date})


    def submitAnswer(self,request):

        """
            this function comapares the user solutions with the solutions stored in the database by

            running queries for each statement and compare the output.

            then display the marks obtained to the user
        
        """
        if request.method == 'POST':
            feedback_data = []
            total_marks_obtained = 0  # Initialize the total marks obtained

            level_marks = {}  # Dictionary to store marks obtained for each level


        

            for key, value in request.POST.items():
                if key.startswith('answers[') and key.endswith(']'):
                    question_id = key.split('[')[1].split(']')[0]

                    try:
                        assignment = GeneratedAssignment.objects.get(pk=int(question_id))
                    except GeneratedAssignment.DoesNotExist:
                        # Handle the case where the GeneratedAssignment with the given pk doesn't exist
                        return render(request,'login_page.html',Authenctication().getUsername(request))

                    expected_answer = assignment.answer
                    user_answer = value
                    marks = assignment.marks
                    level = assignment.level
                    
                    
                    with connection.cursor() as cursor:
                        
                        try:
                            cursor.execute(user_answer)  # Execute user SQL query
                            user_query = cursor.fetchall()

                        except Exception as e:
                            user_query = str(e)
                            
                    
                    with connection.cursor() as trueQuery:
                        
                        try:
                            trueQuery.execute(expected_answer)  # Execute expected SQL query
                            expected_query = trueQuery.fetchall()
                        except Exception as e:
                            expected_query = str(e)

                            # Compare user query result with expected query result
                    marksObtained = 0
                    #test cases passed
                    count = 0
                    totalCount = 0
                    e = None
                    
                    if user_answer!="":
                        if expected_query==user_query:
                            count=100
                            totalCount=100
                        else:
                            for index,item in enumerate(expected_query):
                                try:
                                    if item==user_query[index]:
                                        count += 1
                                        totalCount += 1
                                        print(item==user_query[index])
                                except:
                                    count+=0
                                    totalCount+=1

                        if totalCount > 0:
                            marksObtained = (count / totalCount) * marks
                            if(user_query==expected_query):
                                marksObtained=marks
                            total_marks_obtained += marksObtained
                            
                        #count marks obtained for each level
                        # Update the level_marks dictionary
                        level = assignment.level
                        if level not in level_marks:
                            level_marks[level] = 0
                        level_marks[level] += marksObtained

                        #print(user_query==expected_query,total_marks_obtained)
                    
                    else:
                        marksObtained = 0  # Assign 0 marks for other cases (user_query != expected_query)

                    testCase =str(count)+"/"+str(totalCount)
                    feedback_data.append({
                        'question': assignment.question,
                        'level': level,
                        'expected_answer': "passed test cases: "+testCase,
                        'user_answer': user_answer,
                        'marks_obtained': marksObtained,
                    })

            # #create gradebook
            # Create a Gradebook entry for the user if it doesn't exist
            user  =Authenctication().getUsername(request)
            gradebook, created = Gradebook.objects.get_or_create(studentNum=user)

            if created:
                # Initialize the Gradebook entry if it's newly created
                gradebook.overallMarks = total_marks_obtained
                gradebook.numTemps = 1
                gradebook.easy = level_marks.get('Basic', 0)  # Set to 0 by default if not found in level_marks
                gradebook.intermediate = level_marks.get('Intermediate', 0)  # Set to 0 by default if not found in level_marks
                gradebook.hard = level_marks.get('Advanced', 0)  # Set to 0 by default if not found in level_marks


            # If the Gradebook entry already exists, update it with the latest data
            else:
                if gradebook.overallMarks <= total_marks_obtained:
                    gradebook.overallMarks = total_marks_obtained
                

            # Save the Gradebook entry
            for level, marks in level_marks.items():
                if level == 'Basic':
                    gradebook.easy = marks
                elif level == "Intermediate":
                    gradebook.intermediate = marks
                elif level == "Advanced":
                    gradebook.hard = marks
            gradebook.save()

            # Delete all records in the GeneratedAssignment model
            GeneratedAssignment.objects.all().delete()
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM sqlite_sequence WHERE name = 'GeneratedAssignment'")

            

            return render(request, 'AssignmentFeedback.html', {
                'feedback_data': feedback_data,
                'total_marks_obtained': total_marks_obtained,  # Pass the total marks obtained to the template
            })


    def gradebook(self,request):
        # Get the username or identification number of the user
        user = Authenctication().getUsername(request)

        # Retrieve the student's data from the Gradebook model
        try:
            students = Gradebook.objects.filter(studentNum=user)
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
            easy=0
            intermediate=0
            hard= 0
            
        total = 2*10+3*10+4*10

        # Pass the student data to the template
        return render(request, 'gradebook.html', {'students': students, 'easy': easy, 'intermediate': intermediate, 'hard': hard,'total':total})

    def assignmentConfig(self,request):
        """
            this function allows the admin to setup the assignment

            takes :number of attemps
                : number of questions per level
                : Due Date
        """
        if request.method == 'POST':
            form = AssignmentForm(request.POST)
            if form.is_valid():
                try:
                    assignment_instance = form.save()
                    numAttempts = assignment_instance.numAttempts
                    numQuestions = assignment_instance.numQuestions
                    dueDate = assignment_instance.dueDate
                    
                    assignment = AssignmentSettings(numAttempts=numAttempts,
                                                    numQuestions=numQuestions,
                                                    dueDate=dueDate)
                    assignment.save()
                    
                    success_message = f'Assignment configuration has been saved successfully.(Number of Attempts: {numAttempts}, Number Questions per level: {numQuestions}, Due Date: {dueDate})'
                    messages.success(request, success_message)
                    
                    return redirect('assignmentSetup')
                except Exception as e:
                    messages.error(request, f'An error occurred while saving the assignment configuration: {str(e)}')
            else:
                messages.error(request, 'Form data is not valid. Please check your inputs.')
        else:
            form = AssignmentForm()
        
        return render(request, 'AssignmentSetup.html', {'form': form})