from django.contrib import admin
from .models import TutorialInstitute,TutorialInstitutePlaylist,TutorialTutors,TutorialTutorsPlaylist
# Register your models here.

admin.site.register(TutorialTutorsPlaylist)
admin.site.register(TutorialInstitute)
admin.site.register(TutorialTutors)
admin.site.register(TutorialInstitutePlaylist)