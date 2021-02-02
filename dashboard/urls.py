from django.urls import path
from .views import *


urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('old', dashboard2, name='dashboard-2'),
    path("profileUpdate/", profileUpdate, name="coachingprofile"),
    path('signupTutorContinued/<int:id>',
         signupTutorContinued, name='signupTutorContinued'),
    path("getOTP/", getOTP, name="getOTP"),
]
