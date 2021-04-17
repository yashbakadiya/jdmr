from django.urls import path
from .views import *
from .api import *

urlpatterns = [
    path('teaShowAllNotice/', teaShowAllNotice, name='teaShowAllNotice'),
    path('teaShowNotice/<int:id>', teaShowNotice, name='teaShowNotice'),
    path('addTutors/', addTutors, name='addTutors'),
    path('viewTutors/', viewTutors, name='viewTutors'),
    path('deleteTutor/<int:id>', deleteTutor, name='deleteTutor'),
    path('editTutor/<int:id>', editTutor, name='editTutor'),
    path('archiveTutorList/', archiveTutorList, name='archiveTutorList'),
    path('searchUserTutor/', searchUserTutor, name='searchUserTutor'),
    path('exist/addTutor/<int:id>', AddalreadyExistsTutor,name='AddalreadyExistsTutor'),
    path('viewAssignmentTutor/',viewAssignmentTutor, name='viewAssignmentTutor'),
    path('assign/<int:pk>',assign,name='assign'),
    path('enrolledTutors/', enrolledTutors, name='enrolledTutors'),
    path('Review/Tutor/<tutor_id>', ReviewTutors, name="reviewtutor"),
    path('teaMakeAppointment/<int:id>',teaMakeAppointment, name='teaMakeAppointment'),

    path('rejectTeaAppointment/<int:pk>',rejectAppointment, name='rejectTeaAppointment'),
    path('acceptTeaAppointment/<int:pk>',acceptAppointment, name='acceptTeaAppointment'),

    path('teacherCalendar/', teacherCalendar, name='teacherCalendar'),
    # API Urls
    path('tutor-api', TutorAPI, name="tutor-api"),
    path('searc-tutor-api', SearchTutorAPI, name="search-tutor-api"),
    path('enrolled-tutor-api', EnrolledTutorAPI, name="enrolled-tutor-api"),
    path('review-tutor-api', ReviewTutorAPI, name="review-tutor-api"),
]
