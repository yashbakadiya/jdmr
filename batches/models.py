from django.db import models
from accounts.models import Institute,Teacher,Student
from courses.models import Courses
from students.models import UnconfirmedStudentInst


# Create your models here.
class BatchTiming(models.Model):
    batchName       = models.CharField(max_length=255,default="",unique=True)
    days            = models.CharField(max_length=255,default="",help_text="Comma seperated")
    startTime       = models.CharField(max_length=255,default="")
    endTime         = models.CharField(max_length=255,default="")
    original24time  = models.CharField(max_length=255,default="",help_text="Comma seperated")
    startDate       = models.DateField(null=True,blank=True)
    endDate         = models.DateField(null=True,blank=True)
    createdAt       = models.DateTimeField(auto_now_add=True)
    updatedAt       = models.DateTimeField(auto_now=True)
    institute       = models.ForeignKey(Institute,on_delete=models.CASCADE,related_name='BatchTiming',null=True)
    course          = models.CharField(max_length=150,default="")
    forclass        = models.CharField(max_length=150,default="")
    teachingtype    = models.CharField(max_length=150,default="")

    def __str__(self):
        return self.batchName
    
class BatchTimingTutor(models.Model):
    sno             = models.AutoField(primary_key=True)
    batchName       = models.CharField(max_length=255,default="")
    days            = models.CharField(max_length=255,default="",help_text="Comma seperated")
    startTime       = models.CharField(max_length=255,default="")
    endTime         = models.CharField(max_length=255,default="")
    original24time  = models.CharField(max_length=255,default="",help_text="Comma seperated")
    createdAt       = models.DateTimeField(auto_now_add=True)
    updatedAt       = models.DateTimeField(auto_now=True)
    StartDate       = models.DateTimeField()
    EndDate         = models.DateTimeField()
    Tutor           = models.ForeignKey(Teacher,on_delete=models.SET_NULL,null=True,related_name='BatchTutor')



class Notice(models.Model):
    title               = models.CharField(max_length=35,default="")
    description         = models.TextField()
    createdAt           = models.DateTimeField(auto_now_add=True)
    batch               = models.ForeignKey(BatchTiming,on_delete=models.CASCADE,null=True,related_name='Notice')

    def __str__(self):
        return self.title

class EnrollRequest(models.Model):
    student             = models.ForeignKey(Student,on_delete=models.CASCADE,null=True)
    title               = models.CharField(max_length=35,default="")
    description         = models.TextField()
    createdAt           = models.DateTimeField(auto_now_add=True)
    request             = models.ForeignKey(UnconfirmedStudentInst,on_delete=models.CASCADE,null=True)