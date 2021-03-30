from django.urls import path
from .views import *
from .api import *

urlpatterns = [
    path('add', AddNotesInstitute, name="addnotes"),
    path('View/All', ViewNotesInstitute, name="viewnotes"),
    path('View/<note_id>', PdfViewNoteInstitute, name="PDFviewnoteinstitute"),
    path('Delete/<note_id>', DeleteNoteInstitute, name="DeletenoteInstitute"),
    path('Edit/<note_id>', EditNoteInstitute, name="EditnoteInstitute"),
    # Tutor Notes
    path('Tutor/Notes/add', AddNotesTutor, name="addnotestutor"),
    path('Tutor/Notes/View/All', ViewNotesTutor, name="viewnotestutor"),
    path('Tutor/Notes/Edit/<note_id>', EditNoteTutor, name="editnotetutor"),
    path('Tutor/Notes/Delete/<note_id>',
         DeleteNoteTutor, name="deletenotetutor"),
         
    #Student Notes urls
    path('Student/Notes/All',AllNotesStudent,name="notesstudents"),
    path('Student/Center/note/<note_id>',ViewpdfStudentInstitute,name="viewpdfinstitute"),
    path('Student/Tutor/<note_id>',ViewpdfTutor,name="viewpdftutor"),
    path('getsubjects',subjects,name="subjects"),

    path('Institute/view/<int:pk>',viewInstituteNotesPDF,name="viewinstitutenotespdf"),
    path('Tutor/view/<int:pk>',viewTutorNotesPDF,name="viewtutornotespdf"),

    # API URLs
    path('notes-tutor-api',
         NotesInstituteAPI, name="notes-tutor-api"),
    path('notes-institute-api',
         NotesTutorAPI, name="notes-institute-api"),
]
