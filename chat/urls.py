from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:room_name>/<str:ts>/', views.room, name='room'),
    path('<str:room_name>/<str:ts>/chatsend', views.send, name='send'),
    path('<str:room_name>/<str:ts>/upload1',views.upload1,name='upload1'), 
    path('<str:room_name>/<str:ts>/chatsend2', views.send, name='send2'),
    path('<str:room_name>/<str:ts>/upload2',views.upload1,name='upload1'),
    #path('<str:room_name>/upload2',views.upload1,name='upload1'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
  urlpatterns += staticfiles_urlpatterns()