from django.db import models
from accounts.models import Institute,Teacher
from courses.models import Courses


# Create your models here.
class BatchTiming(models.Model):
    batchName       = models.CharField(max_length=255,default="",unique=True)
    days            = models.CharField(max_length=255,default="",help_text="Comma seperated")
    startTime       = models.CharField(max_length=255,default="")
    endTime         = models.CharField(max_length=255,default="")
    original24time  = models.CharField(max_length=255,default="",help_text="Comma seperated")
    createdAt       = models.DateTimeField(auto_now_add=True)
    updatedAt       = models.DateTimeField(auto_now=True)
    institute       = models.ForeignKey(Institute,on_delete=models.CASCADE,related_name='BatchTiming')
    course          = models.ForeignKey(Courses,on_delete=models.CASCADE,related_name="BatchCourse")
    forclass        = models.CharField(max_length=150,default="")

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
