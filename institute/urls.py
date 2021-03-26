from django.urls import path
from .views import *

urlpatterns = [
    path("endrolledINstitute/",instituteTutor,name="EndrolledInstitute"),
    path('searchCoachingCenter/',searchCoachingCenter,name='searchCoachingCenter'),
    path('Review/Institutes/<inst_id>',ReviewInstitute,name="reviewinstitute"),
    path('institutecalendar',institutecalendar,name="institutecalendar"),
    path('dateandbatch',dateandbatch,name="dateandbatch"),
    path('instCalendar',instCalendar, name="instCalendar"),

   
    ]
