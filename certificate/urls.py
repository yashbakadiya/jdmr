from django.urls import path
from .import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('<certificate_num>/', views.certificatenum, name='certificatenum'),
    path('get-certificate', views.view_certi, name='view_certificate'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
