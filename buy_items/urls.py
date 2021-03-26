from django.urls import path
from .views import buyInstituteNotes,buyTutorNotes, buyInstituteTutorial, buyTutorTutorial


urlpatterns = [
    path('buyInstituteNotes/<int:id>', buyInstituteNotes, name='buyInstituteNotes'),
    path('buyTutorNotes/<int:id>', buyTutorNotes, name='buyTutorNotes'),
    path('buyInstituteTutorial/<int:id>', buyInstituteTutorial ,name='buyInstituteTutorial'),
    path('buyTutorTutorial/<int:id>', buyTutorTutorial ,name='buyTutorTutorial'),
]
