from django.contrib import admin
from .models import AddStudentInst,PostTution,PostAssignment,UnconfirmedStudentInst
# Register your models here.

admin.site.register(AddStudentInst)
admin.site.register(PostTution)
admin.site.register(PostAssignment)
admin.site.register(UnconfirmedStudentInst)
