from django.urls import path
from .views import *
from .api import *


urlpatterns = [
    path('buyInstituteNotes/<int:id>', buyInstituteNotes, name='buyInstituteNotes'),
    path('buyTutorNotes/<int:id>', buyTutorNotes, name='buyTutorNotes'),
    path('buyTutorExam/<int:id>', buyTutorExam, name='buyTutorExam'),
    path('buyInstituteTutorial/<int:id>', buyInstituteTutorial ,name='buyInstituteTutorial'),
    path('buyTutorTutorial/<int:id>', buyTutorTutorial ,name='buyTutorTutorial'),
    #show revenue
    path('Earnings', revenueShow ,name='earnings'),



    path('buyInstituteNotesAPI/<int:id>', buyInstituteNotesAPI, name='buyInstituteNotesAPI'),
    path('buyTutorNotesAPI/<int:id>', buyTutorNotesAPI, name='buyTutorNotesAPI'),
    path('buyTutorExamAPI/<int:id>', buyTutorExamAPI, name='buyTutorExamAPI'),
    path('buyInstituteTutorialAPI/<int:id>', buyInstituteTutorialAPI ,name='buyInstituteTutorialAPI'),
    path('buyTutorTutorialAPI/<int:id>', buyTutorTutorialAPI ,name='buyTutorTutorialAPI'),
]
