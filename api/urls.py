from django.urls import path, include
from . import views

app_name = 'api'

urlpatterns = [
    # AUTH
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    # Models

]
