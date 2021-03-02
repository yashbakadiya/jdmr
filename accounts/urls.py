from django.urls import path
from .views import *
from .api import loginApi, SignUpAPI
from django.contrib.auth import views as auth_views




urlpatterns = [
    path("", testing, name="Testing"),
    path("login", login, name="Login"),
    path("signup", signup, name="Signup"),
    path("logout", logout, name="Logout"),
    path('loginapi', loginApi, name="loginApi"),
    path('signup-api', SignUpAPI, name="signup-api"),
   # path('forgot-password',forgotpassword, name="forgot-password"),
    # Change Password
    path('change-password/',auth_views.PasswordChangeView.as_view(
              template_name='accounts/change-password.html',
            success_url = '/' ),name='change-password'
        ),

     # Forget Password
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='accounts/password_reset.html',
             subject_template_name='accounts/password_reset_subject.txt',
             email_template_name='accounts/password_reset_email.html',
            # success_url='/login/'
         ),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='accounts/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='accounts/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/', 
         auth_views.PasswordResetCompleteView.as_view(
             template_name='accounts/password_reset_complete.html'
         ),
         name='password_reset_complete'),
    
    
]
