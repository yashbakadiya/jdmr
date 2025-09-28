from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView


urlpatterns = [
    path('chat/', include('chat.urls')),
    path('admin/', admin.site.urls),
    path('', include('code2learn_app.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('courses/', include('courses.urls')),
    path('batches/', include('batches.urls')),
    path('teacher/', include('teacher.urls')),
    path('institute/', include('institute.urls')),
    path('students/', include('students.urls')),
    path('tutorials/', include('tutorials.urls')),
    path('results/', include('results.urls')),
    path('exams/', include('exams.urls')),
    path('notes/', include('notes.urls')),
    path('fees/', include('fees.urls')),
    path('accounts/', include('accounts.urls')),
    path('buy/', include('buy_items.urls')),
    path('certificate/', include('certificate.urls')),
    path('auth/', include('users.urls')),
    path('blog/', include('blog.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name="gettoken"),
    path('api/token/refresh/', TokenRefreshView.as_view()),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    #path('api/token/verify/', TokenVerifyView.as_view()),
