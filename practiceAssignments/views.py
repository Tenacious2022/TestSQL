import random
from django.db import connection
from django.http import JsonResponse
from django.shortcuts import redirect, render
from assignments.models import BasicSQL, IntermediateSQL, AdvancedSQL
from assignments.views import  Assignment
from django.views.decorators.csrf import csrf_exempt
import json

class PracticeAssignment:

    def getDatabaseSize(self,request):
        """
        Calculates the lengths of questions in each difficulty levels (basic, intermediate, advanced).

        Returns:
            dict: A dictionary containing lists of lengths for each difficulty levels (basic, intermediate, advanced) in the database.
        """
        sizeData = {
            'easySize': BasicSQL.objects.count(),
            'intermediateSize': IntermediateSQL.objects.count(),
            'advancedSize': AdvancedSQL.objects.count()
        }
        return JsonResponse(sizeData)



    def generateAssignment(self):
        """
        Generate questions using random PKs generated above for different levels (basic, intermediate, advanced)
        and store them in lists.

        Returns:
            dict: A dictionary containing lists of random questions, answers, marks for each level.
        """
    
        levels = Assignment().randomiseQuestions(10)

        questions = {
            'Basic': levels['basicQuestions'],
            'Intermediate': levels['intermediateQuestions'],
            'Advanced': levels['advancedQuestions'],
        }

        questionsData = {}

        for level, levelItems in questions.items():
            questionList = []
            for i in levelItems:
                tab = level + "SQL"
                questionObj = PracticeAssignment().get_question_object(tab, i)
                question = questionObj.question
                solution = questionObj.answer
                marks = questionObj.marks

                questionList.append({'question': question, 'answer': solution, 'marks': marks, 'level': level})

            questionsData[level] = questionList

        return questionsData

    def get_question_object(self,tab, i):

        """
            randomly selects questions from the database
        """
        if tab == 'BasicSQL':
            return BasicSQL.objects.get(pk=i)
        elif tab == 'IntermediateSQL':
            return IntermediateSQL.objects.get(pk=i)
        elif tab == 'AdvancedSQL':
            return AdvancedSQL.objects.get(pk=i)

    def displayQuestions(self,request):

        """
            returns questions generated to the frontend
        """
        assignment_data = PracticeAssignment().generateAssignment()
        return JsonResponse(assignment_data)


    def select_questions(self,request):

        """
            this method returns number of questions selected by user per level
        """
        if request.method == 'POST':
            easy = int(request.POST.get('easy', 0))
            medium = int(request.POST.get('medium', 0))
            hard = int(request.POST.get('hard', 0))
            request.session['easy'] = easy
            request.session['medium'] = medium
            request.session['hard'] = hard

        return render(request, 'select_questions.html')

    @csrf_exempt
    def submit_feedback(self,request):
        """
            this method selects answers from the user and make a comparison with answers
            stored in the database and test different cases to check if they all pass

            return: feeback
        """
        if request.method == 'POST':

            try:
                data = json.loads(request.body)
                questions = data['arrayQuestions']
                levels = data['levels']
                user_answers = data['usersAnswers']

                feedback_data = []
                total_marks_obtained = 0 

                for index, question in enumerate(questions):

                    userAnswer = user_answers[index]
                    level = levels[index]
                    
                    if not userAnswer:
                        marksObtained = 0
                        total_marks_obtained += marksObtained
                        feedback_data.append({
                            'question': question,
                            'level': levels[index],
                            'expected_answer': "Test Cases Passed: 0/100",
                            'user_answer': userAnswer,
                            'marks_obtained': marksObtained,
                        })
                        continue 

                    if level == 'Basic':
                        db = BasicSQL
                    elif level == 'Intermediate':
                        db = IntermediateSQL
                    elif level == 'Advanced':
                        db = AdvancedSQL
                    else:
                        continue
                    
                    result = db.objects.filter(question=question).first()

                    expected_answer = result.answer
                    marks = result.marks

                    with connection.cursor() as testQuery:
                        
                        try:
                            testQuery.execute(userAnswer)  
                            user_query = testQuery.fetchall()

                        except Exception as e:
                            user_query = str(e)
                            
                    with connection.cursor() as trueQuery:
                        
                        try:
                            trueQuery.execute(expected_answer)  
                            expected_query = trueQuery.fetchall()
                        except Exception as e:
                            expected_query = str(e)
            
                    marksObtained = 0

                    e = None

                    count=0
                    totalCount=100

                    if expected_query==user_query:
                        count=100
                        totalCount=100
                        marksObtained=marks
                        total_marks_obtained+=marksObtained
                    
                    print(index,question,userAnswer)

                    testCase =str(count)+"/"+str(totalCount)
                    feedback_data.append({
                        'question': question,
                        'level': levels[index],
                        'expected_answer': "Test Cases Passed: "+testCase,
                        'user_answer': userAnswer,
                        'marks_obtained': marksObtained,
                    })
            
                response_data = {
                    'feedback_data': feedback_data,
                    'total_marks_obtained': total_marks_obtained, 
                }
                return JsonResponse(response_data)

            except Exception as e:
                response_data = {
                    'error': str(e),
                    'message': 'Error while submitting feedback'
                }
                return JsonResponse(response_data, status=500)
                
