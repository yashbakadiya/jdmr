from django.urls import path
from .views import *
from .api import *


urlpatterns = [
    path('Add', addTutorialsInstitute, name="addtutorials"),
    path('viewTutorials', ViewTutorials, name="viewtutorials"),
    path('Archive', ArchiveTutorials, name="archivetutorials"),
    path('Add/Videos/<course_id>', addTutorialsInstituteVideos, name="addplaylist"),
    path('delete/<course_id>', DeleteTutorialsInstitute, name="deletetutorial"),
    path('Edit/<course_id>', EditTutorialsInstitute, name="editTutorial"),
    path('Watch/<course_id>', WatchTutorialsInstitute, name="viewtutorial"),
    path('Watch/Delete/<playlist_id>',
         DeleteTutorialsInstituteVideos, name="deleteplaylistvideo"),
    path('Watch/Edit/<playlist_id>',
         EditTutorialsInstituteVideos, name="editTutorialvideos"),
    path('Tutor/add', addTutorialsTutor, name='tutorialstutor'),
    path('Tutor/Add/Videos/<course_id>',
         addTutorialsTutorVideos, name='addvideosTutor'),
    path('Tutor/viewTutorials', ViewTutorialsTutor, name="viewtutorialstutor"),
    path('Tutor/Watch/<course_id>', WatchTutorialsTutor, name="viewtutorialtutor"),
    path('Tutor/delete/<course_id>', DeleteTutorialsTutor,
         name="deletetutorialstutor"),
    path('Tutor/Edit/<course_id>', EditTutorialsTutor, name="editTutorialtutor"),
    path('Tutor/Archive', ArchiveTutorialsTutor, name="Archivetutorialstutor"),
    path('Tutor/Watch/Delete/<playlist_id>',
         DeleteTutorialsTutorVideos, name="deleteplaylistvideotutor"),
    path('Tutor/Watch/Edit/<playlist_id>',
         EditTutorialsTutorVideos, name="editTutorialvideostutor"),
    path('tutorials/search', SearchCourses, name="searchcourses"),
    path('tutorials/Student/Watch/<course_id>',
         WatchTutorTutorials, name="watchTutorcourse"),
    path('tutorials/Student/Watch/Institute/<course_id>',
         WatchInstituteTutorials, name="watchInstitutecourse"),

    # API URLs

    path('add-tutorial-institute-api',
         AddTutorialInstituteAPI, name="add-tutorial-institute-api"),
    path('view-tutorial-institute-api',
         ViewTutorialsAPI, name="view-tutorial-api"),
    path('archive-tutorial-api',
         ArchiveTutorialsAPI, name="archive-tutorial-api"),
    path('add-tutorial-institute-video-api',
         AddTutorialsInstituteVideosAPI, name="add-tutorial-institute-video-api"),
    path('delete-tutorial-institute-api',
         DeleteTutorialsInstituteAPI, name="delete-tutorial-institute-api"),
    path('edit-tutorial-institute-api',
         EditTutorialsInstituteAPI, name="edit-tutorial-institute-api"),
    path('watch-tutorial-institute-api',
         WatchTutorialsInstituteAPI, name="watch-tutorial-institute-api"),
    path('delete-tutorial-institute-videos-api',
         DeleteTutorialsInstituteVideosAPI, name="delete-tutorial-videos-api"),
    path('edit-tutorial-institute-video-api',
         EditTutorialsInstituteVideoAPI, name="edit-tutorial-institute-video-api"),
    path('add-tutorial-tutor-api',
         AddTutorialsTutorAPI, name="add-tutorial-tutor-api"),
    path('view-tutorial-tutor-api',
         ViewTutorialsTutorAPI, name="view-tutorial-tutor-api"),
    path('watch-tutorial-tutor-api',
         WatchTutorialsTutorAPI, name="watch-tutorial-tutor-api"),
    path('delete-tutorial-tutor-api',
         DeleteTutorialsTutorAPI, name="delete-tutorial-tutor-api"),
    path('edit-tutorial-tutor-api',
         EditTutorialsTutorAPI, name="edit-tutorial-tutor-api"),
    path('delete-tutorial-tutor-video-api',
         DeleteTutorialsTutorVideosAPI, name="delete-tutorial-tutor-video-api"),
    path('edit-tutorial-tutor-video-api',
         EditTutorialsTutorVideosAPI, name="edit-tutorial-tutor-video-api"),
    path('archive-tutorial-tutor-api',
         ArchiveTutorialsTutorAPI, name="archive-tutorial-tutor-api"),
]
