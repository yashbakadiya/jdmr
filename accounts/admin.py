from django.contrib import admin
from .models import Institute,Teacher,Student,Tutorid, User
# Register your models here.

admin.site.register(Institute)
admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Tutorid)
admin.site.register(User)
