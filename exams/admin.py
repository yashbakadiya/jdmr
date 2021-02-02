from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Exam)
admin.site.register(TutorExam)
admin.site.register(MultipleAnswer)
admin.site.register(MultipleQuestion)
admin.site.register(ShortAnswerQuestion)
admin.site.register(LongAnswerQuestion)
admin.site.register(BooleanQuestion)
admin.site.register(TutorBooleanQuestion)
admin.site.register(TutorLongAnswerQuestion)
admin.site.register(TutorMultipleQuestion)
admin.site.register(TutorShortAnswerQuestion)
admin.site.register(StudentAnswer)
admin.site.register(StudentExamResult)
admin.site.register(StudentMapping)
