from .api import CoachingResultStudentAPI
from django.urls import path
from .views import *

urlpatterns = [
    #Student Result
    path('Student/Exams/Result/All',ViewExamsResult,name="studentexamresults"),
    path('Student/Exam/Result/Detailed/Report/<int:pk>',detailed_result,name="detailed_report"),
    path('Student/Tutor/Exam/Result/Detailed/Report/<int:pk>',tutor_detailed_result,name="tutor_detailed_report"),
    path('All', CoachingResultStudent, name="centerexamresults"),
    path('All-api', CoachingResultStudentAPI, name="centerexamresults-api"),

    path('Center/Exams/Result/All',CoachingResultStudent,name="centerexamresults"),
    path('Center/Exams/Result/Exam/<exam_id>',GetExamResults,name="getexamresults"),
    path('Center/Exam/Result/Student/<student_id>/<exam_id>',GetStudentResults,name="studentresult"),
    path('Center/Result/Review/Answer/<question_id>',Review_Answer,name="check_answer"),
    path('Center/Result/Anotate/<id>/<pk>',webViewerAnnotate,name="anotatePdfViewer"),
    path('Center/Result/Anotate/pdf/<id>/<pk>',annotateAnswers,name="anotate"),

    path('Tutor/Exams/Result/All',TutorResultStudent,name="tutorexamresults"),
    path('Tutor/Exams/Result/Exam/<exam_id>',TutorGetExamResults,name="tutorgetexamresults"),
    path('Tutor/Exam/Result/Student/<student_id>/<exam_id>',TutorGetStudentResults,name="tutorstudentresult"),
    path('Tutor/Result/Review/Answer/<question_id>',TutorReview_Answer,name="tutorcheck_answer"),
    path('Tutor/Result/Anotate/<id>/<pk>',TutorwebViewerAnnotate,name="tutoranotatePdfViewer"),
    path('Tutor/Result/Anotate/pdf/<id>/<pk>',TutorannotateAnswers,name="tutoranotate"),
]

