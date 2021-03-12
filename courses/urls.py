from django.urls import path
from .views import *
from .api import CourseAPI, TeachingTypeAPI


urlpatterns = [
    # path('addCourses/', addCourses, name='AddCourses'),
    path('', courses, name='courses'),
   # path('course-unarchive/<int:id>', courseunArchive, name='course-unarchive'),
    path('course-archive', courseArchive, name='course-archive'),
    path('teach-archive', teachArchive, name='teach-archive'),
    path('teach-unarchive/<int:id>', teachUnArchive, name='teach-unarchive'),
    path('course-unarchive/<int:id>', courseUnArchive, name='course-unarchive'),
    path('courseArchivefirst/<int:id>', courseArchivefirst, name='courseArchivefirst'),
    path('teaching-type', teachingType2, name='teaching-type-2'),
    path('teachingArchive/<int:id>',teachingArchive,name='teachingArchive'),

    path('classes', FindCoursesclass, name="findCourseclass"), #altered
    path('addCourse-api', CourseAPI, name='AddCoursesAPI'),
    path('viewCourses/', viewCourses, name='viewCourses'),
    path('archiveCourseList/', archiveCourseList, name='archiveCourseList'),
    path('deleteCourse/<int:id>', deleteCourse, name='deleteCourse'),
    path('deleteteaching/<int:id>', deleteteaching, name= 'deleteteaching' ),
    path('editCourse/<int:id>', editCourse, name='editCourse'),
    path('teachingType/', teachingType, name='teachingType'),
    path('teachingType-api/', TeachingTypeAPI, name='teachingTypeAPI'),
    path('viewteachType/', viewteachType, name='viewteachType'),
    path('editTeachingType/<int:id>', editTeachingType, name='editTeachingType'),
    
]

