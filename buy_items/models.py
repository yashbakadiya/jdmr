from django.db import models
from accounts.models import Student
from tutorials.models import TutorialInstitute
from notes.models import NotesInstitute, NotesTutor

class BuyInstituteNotes(models.Model):
    student = models.ForeignKey(to=Student, on_delete=models.SET_NULL, null=True)
    note = models.ForeignKey(to=NotesInstitute, on_delete=models.SET_NULL, null=True)
    status = models.BooleanField(default=0, null=True)
    buy_at = models.DateField(auto_now_add=True)
    order_id = models.CharField(unique=True, max_length=100, null=True, blank=True)

    class Meta:
        unique_together = [['note', 'student']]

    def __str__(self):
        return str(self.note.title) + str(self.student.id)

class BuyTutorNotes(models.Model):
    student = models.ForeignKey(to=Student, on_delete=models.SET_NULL, null=True)
    note = models.ForeignKey(to=NotesTutor, on_delete=models.SET_NULL, null=True)
    status = models.BooleanField(default=0, null=True)
    buy_at = models.DateField(auto_now_add=True)
    order_id = models.CharField(unique=True, max_length=100, null=True, blank=True)

    class Meta:
        unique_together = [['note', 'student']]

    def __str__(self):
        return str(self.note.title) + str(self.student.id)

class BuyTutorial(models.Model):
    student = models.ForeignKey(to=Student, on_delete=models.SET_NULL, null=True)
    tutorial = models.ForeignKey(to=TutorialInstitute, on_delete=models.SET_NULL, null=True)
    status = models.BooleanField(default=0 ,null=True)
    buy_at = models.DateField(auto_now_add=True)
    amount = models.IntegerField(default=0, null=True)
    order_id = models.CharField(unique=True, max_length=100, null=True, blank=True)

    class Meta:
        unique_together = [['tutorial', 'student']]

    def __str__(self):
        return str(self.tutorial.Title) + str(self.student.id)
    
    
