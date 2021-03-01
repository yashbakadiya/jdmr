from django.db import models
from accounts.models import Institute,Teacher,Student
from django.urls import reverse
# Create your models here.
class NotesInstitute(models.Model):
    institute = models.ForeignKey(Institute,related_name='centernotes',on_delete=models.CASCADE)
    notes = models.FileField(upload_to="notes/Institute")
    title = models.CharField(max_length=2000)
    subject = models.CharField(max_length=3000)
    forclass = models.CharField(max_length=150, default="")
    description = models.TextField()
        
    def __str__(self):
        return f"notes"
    
    @property
    def View_pdf(self):
        return reverse('viewpdfinstitute', args=(self.id,))


class NotesTutor(models.Model):
    tutor = models.ForeignKey(Teacher,related_name='tutornotes',on_delete=models.CASCADE)
    notes = models.FileField(upload_to="notes/Institute")
    title = models.CharField(max_length=2000)
    subject = models.CharField(max_length=3000)
    description = models.TextField()
        
    def __str__(self):
        return f"notes"

    @property
    def View_pdf(self):
        return reverse('viewpdftutor', args=(self.id,))