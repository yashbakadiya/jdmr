from .api import CoachingResultStudentAPI
from django.urls import path
from .views import *

urlpatterns = [
    #Student Result
    path('Student/Exams/Result/All',ViewExamsResult,name="studentexamresults"),
    path('Student/Exam/Result/Detailed/Report/<int:pk>',detailed_result,name="detailed_report"),
    path('All', CoachingResultStudent, name="centerexamresults"),
    path('All-api', CoachingResultStudentAPI, name="centerexamresults-api"),
]
