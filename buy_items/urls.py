from django.urls import path
from .views import buyInstituteNotes

urlpatterns = [
    path('buyInstituteNotes/<int:id>', buyInstituteNotes, name='buyInstituteNotes'),
]
