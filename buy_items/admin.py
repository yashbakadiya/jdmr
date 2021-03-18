from django.contrib import admin
from .models import BuyTutorNotes,BuyInstituteNotes, BuyTutorial

admin.site.register(BuyTutorNotes)
admin.site.register(BuyInstituteNotes)
admin.site.register(BuyTutorial)