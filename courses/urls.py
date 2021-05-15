from django.urls import path
from .views import *
from .api import CourseAPI, TeachingTypeAPI


urlpatterns = [
    # path('addCourses/', addCourses, name='AddCourses'),
    path('', courses, name='courses'),
    path('editCourse/<int:id>', editCourse, name='editCourse'),
    path('deleteCourse/<int:id>', deleteCourse, name='deleteCourse'),
    path('courseArchivefirst/<int:id>', courseArchive, name='courseArchivefirst'),
    path('course-archive', courseArchiveList, name='course-archive'),
    path('course-unarchive/<int:id>', courseUnArchive, name='course-unarchive'),
    path('teaching-type', teachingType2, name='teaching-type-2'),
    path('editTeachingType/<int:id>', editTeachingType, name='editTeachingType'),
    path('deleteteaching/<int:id>', deleteteaching, name= 'deleteteaching' ),
    path('teachingArchive/<int:id>',teachingArchive,name='teachingArchive'),
    path('teach-archive', teachArchiveList, name='teach-archive'),
    path('teach-unarchive/<int:id>', teachUnArchive, name='teach-unarchive'),

    path('classes', FindCoursesclass, name="findCourseclass"), #altered
    path('addCourse-api', CourseAPI, name='AddCoursesAPI'),
    # path('viewCourses/', viewCourses, name='viewCourses'),
    # path('archiveCourseList/', archiveCourseList, name='archiveCourseList'),
    # path('teachingType/', teachingType, name='teachingType'),
    path('teachingType-api/', TeachingTypeAPI, name='teachingTypeAPI'),
    # path('viewteachType/', viewteachType, name='viewteachType'),
    
]

