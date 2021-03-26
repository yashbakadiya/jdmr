from django.urls import path
from .views import buyInstituteNotes,buyTutorNotes

urlpatterns = [
    path('buyInstituteNotes/<int:id>', buyInstituteNotes, name='buyInstituteNotes'),
    path('buyTutorNotes/<int:id>', buyTutorNotes, name='buyTutorNotes'),
]
