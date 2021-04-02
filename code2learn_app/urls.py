from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .import views
from code2learn_app.middlewares.auth import auth_middleware


urlpatterns = [
    path('',views.main,name="main"),
    path("home", views.index, name='home'),
    path('InstitutePage',views.InstitutePage, name='InstitutePage'),
    path('StudentPage',views.StudentPage, name='StudentPage'),
    path('TutorPage',views.TutorPage, name='TutorPage'),
    # path("explore-courses", views.course_page, name='explore_courses'),
    # path("search-courses", views.course_search, name='search_courses'),
    # path('invoice', views.invoice, name='invoice'),
    # path('yourinvoice/<str:id>', views.show_invoice, name='show_invoice'),
    # path('register', views.register, name='register'),
    # path('load_courses', views.load_courses, name='load_courses'),
    # path('load_languages', views.load_languages, name='load_languages'),
    # path('load_amount', views.load_amount, name='load_amount'),
    # path('enroll-course/<int:course_id>', auth_middleware(views.enroll_course), name='enroll_course'),
    # path('getcontent', views.getcontent, name='getcontent'),
    # path("handlerequest/", views.handlerequest, name="HandleRequest"),
    # path("razorhandlerequest/", views.Razorhandlerequest, name="razorHandleRequest"),
    # path('career', views.career, name='career'),
    # path('razorpay', views.Razorpay, name='razorpay'),
    # path('failed', views.failed_payment, name='failed_payment'),
]
