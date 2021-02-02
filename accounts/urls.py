from django.urls import path
from .views import *
from .api import loginApi, SignUpAPI


urlpatterns = [
    path("", testing, name="Testing"),
    path("login", login, name="Login"),
    path("signup", signup, name="Signup"),
    path("logout", logout, name="Logout"),
    path('loginapi', loginApi, name="loginApi"),
    path('signup-api', SignUpAPI, name="signup-api"),
]
