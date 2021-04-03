from django.urls import path
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views

urlpatterns = [
    path('<str:name>/<str:ts>/', views.index, name='index'),
    path('<str:name>/<str:ts>/<str:room_name>/', views.room, name='room'),
    path('<str:name>/<str:ts>/<str:room_name>/chatsend', views.send, name='send'),
    path('<str:name>/<str:ts>/<str:room_name>/upload1',views.upload1,name='upload1'), 
    path('<str:name>/<str:ts>/<str:room_name>/chatsend2', views.send, name='send2'),
    path('<str:name>/<str:ts>/<str:room_name>/upload2',views.upload1,name='upload1'),
    #path('<str:room_name>/upload2',views.upload1,name='upload1'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
  urlpatterns += staticfiles_urlpatterns()

# urlpatterns += patterns('django.views.static',(r'^media/(?P<path>.*)','serve',{'document_root':settings.MEDIA_ROOT}), )
