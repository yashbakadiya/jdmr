from django.urls import path
from .import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('all-posts/', views.all_posts, name="all_posts"),
    path('all-posts/<slug:slug>', views.blog_single, name='blog_single'),
    path('search/', views.search, name="search"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
