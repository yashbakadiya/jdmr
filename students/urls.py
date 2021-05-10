from django.urls import path
from .views import *
from .api import *

urlpatterns = [
    path('stuShowAllNotice/', stuShowAllNotice, name='stuShowAllNotice'),
    path('stuShowNotice/<int:id>', stuShowNotice, name='stuShowNotice'),
    path('addStudents/', addStudents, name='addStudents'),
    path('viewStudents/', viewStudents, name='viewStudents'),
    path('deleteStudent/<int:id>', deleteStudent, name="deleteStudent"),
    path('editStudent/<int:id>', editStudent, name="editStudent"),
    path('archiveStudentList/', archiveStudentList, name='archiveStudentList'),
    path('searchUserStudent/', searchUserStudent, name='searchUserStudent'),
    path('exist/addStudents/<int:id>', AddalreadyExistsStudent,name='AddalreadyExistsStudent'),
    path('StudentCalendar/', StudentCalendar, name='StudentCalendar'),
    path('postAssignment/', postAssignment, name='postAssignment'),
    path('extend/<int:id>/',extendDeadline,name="extend"),
    path('postTution/', postTution, name='postTution'),
    path('delete-Assignment/<int:sno>/', delete_Assignment, name='Delete_Assignment'),
    path('delete-Tution/<int:sno>/', delete_Tution, name='Delete_Tution'),
    path('enrolledStudents/',enrolledStudents, name='enrolledStudents'),
    path('stuMakeAppointment/<int:id>',stuMakeAppointment, name='stuMakeAppointment'),
    path('rejectAppointment/<int:pk>',rejectAppointment, name='rejectAppointment'),
    path('acceptAppointment/<int:pk>',acceptAppointment, name='acceptAppointment'),
    # API URLs
    path('add-student-inst-api', AddStudentInstAPI, name='add-student-inst-api'),
    path('view-student-inst-api', ViewStudentInstAPI, name='view-student-inst-api'),
    path('delete-student-inst-api', DeleteStudentInstAPI,name='delete-student-inst-api'),
    path('archive-student-inst-api', ArchiveStudentInstAPI,  name='archive-student-inst-api'),
    path('edit-student-api', EditStudentAPI, name='edit-student-api'),
    path('search-user-student-api', SearchUserStudentAPI, name='search-student-api'),
    path('add-already-exists-student-api', AddalreadyExistsStudentAPI, name='add-already-exists-student-api'),
    path('post-assignment-api', PostAssignmentAPI, name='post-assignment-api'),
    path('post-tution-api', PostTutionAPI, name='post-tution-api'),
    path('view-assignment-api', ViewAssignmentAPI, name='view-assignment-api'),
    path('view-tution-api', ViewTutionAPI, name='view-tution-api'),
]
