from django.contrib import admin
from .models import BuyTutorNotes,BuyInstituteNotes, BuyTutorTutorial, BuyInstituteTutorial, Revenue

admin.site.register(BuyTutorNotes)
admin.site.register(BuyInstituteNotes)
admin.site.register(BuyTutorTutorial)
admin.site.register(BuyInstituteTutorial)
admin.site.register(Revenue)
