from .api import CoachingResultStudentAPI
from django.urls import path
from .views import *

urlpatterns = [
    #Student Result
    path('Student/Exams/Result/All',ViewExamsResult,name="studentexamresults"),
    path('Student/Exam/Result/Detailed/Report/<int:pk>',detailed_result,name="detailed_report"),
    path('All', CoachingResultStudent, name="centerexamresults"),
    path('All-api', CoachingResultStudentAPI, name="centerexamresults-api"),

    path('Center/Exams/Result/All',CoachingResultStudent,name="centerexamresults"),
    path('Center/Exams/Result/Exam/<exam_id>',GetExamResults,name="getexamresults"),
    path('Center/Exam/Result/Student/<student_id>/<exam_id>',GetStudentResults,name="studentresult"),
    path('Center/Result/Review/Answer/<question_id>',Review_Answer,name="check_answer"),
    path('Center/Result/Anotate/<id>/<pk>',webViewerAnnotate,name="anotatePdfViewer"),
    path('Center/Result/Anotate/pdf/<id>/<pk>',annotateAnswers,name="anotate"),
]

