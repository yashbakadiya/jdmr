from django.urls import path
from .import views
from django.views.decorators.csrf import csrf_exempt
from code2learn_app.middlewares.auth import auth_middleware

# from django.conf import settings
# from django.conf.urls.static import static

urlpatterns = [
    path('validate-email/', csrf_exempt(views.email_validation), name='email_validate'),
    path('validate-password/', csrf_exempt(views.password_validation), name='password_validate'),
    path('find-email/', csrf_exempt(views.find_email), name='find_email'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.logout, name='logout'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('send-otp/', views.send_otp, name='send_otp'),
    path('check-otp/', views.check_otp, name='check_otp')
]
