import uuid

from django.db import models
from accounts.models import Student
from tutorials.models import TutorialInstitute, TutorialTutors
from notes.models import NotesInstitute, NotesTutor
from exams.models import TutorExam

class BuyInstituteNotes(models.Model):
    student = models.ForeignKey(to=Student, on_delete=models.CASCADE, null=True)
    note = models.ForeignKey(to=NotesInstitute, on_delete=models.CASCADE, null=True)
    status = models.BooleanField(default=0, null=True)
    buy_at = models.DateField(auto_now_add=True)
    order_id = models.UUIDField(default=uuid.uuid4, unique=True, db_index=True, editable=False)

    class Meta:
        unique_together = [['note', 'student']]

    def __str__(self):
        return str(self.note.title) + str(self.student.id)

class BuyTutorNotes(models.Model):
    student = models.ForeignKey(to=Student, on_delete=models.CASCADE, null=True)
    note = models.ForeignKey(to=NotesTutor, on_delete=models.CASCADE, null=True)
    status = models.BooleanField(default=0, null=True)
    buy_at = models.DateField(auto_now_add=True)
    order_id = models.UUIDField(default=uuid.uuid4, unique=True, db_index=True, editable=False)

    class Meta:
        unique_together = [['note', 'student']]

    def __str__(self):
        return str(self.note.title) + str(self.student.id)

class BuyTutorTutorial(models.Model):
    student = models.ForeignKey(to=Student, on_delete=models.CASCADE, null=True)
    tutorial = models.ForeignKey(to=TutorialTutors, on_delete=models.CASCADE, null=True)
    status = models.BooleanField(default=0 ,null=True)
    buy_at = models.DateField(auto_now_add=True)
    order_id = models.UUIDField(default=uuid.uuid4, unique=True, db_index=True, editable=False)

    class Meta:
        unique_together = [['tutorial', 'student']]

    def __str__(self):
        return str(self.tutorial.Title) + str(self.student.id)


class BuyInstituteTutorial(models.Model):
    student = models.ForeignKey(to=Student, on_delete=models.CASCADE, null=True)
    tutorial = models.ForeignKey(to=TutorialInstitute, on_delete=models.CASCADE, null=True)
    status = models.BooleanField(default=0 ,null=True)
    buy_at = models.DateField(auto_now_add=True)
    order_id = models.UUIDField(default=uuid.uuid4, unique=True, db_index=True, editable=False)

    class Meta:
        unique_together = [['tutorial', 'student']]

    def __str__(self):
        return str(self.tutorial.Title) + str(self.student.id)


class BuyTutorExam(models.Model):
    student = models.ForeignKey(to=Student, on_delete=models.CASCADE, null=True)
    exam = models.ForeignKey(to=TutorExam , on_delete=models.CASCADE, null=True)
    status = models.BooleanField(default=0, null=True)
    buy_at = models.DateField(auto_now_add=True)
    order_id = models.UUIDField(default=uuid.uuid4, unique=True, db_index=True, editable=False)

    class Meta:
        unique_together = [['student', 'exam']]
    
    def __str__(self):
        return str(self.exam.courseName) + str(self.student.id)

