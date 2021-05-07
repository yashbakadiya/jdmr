from django.db import models
from accounts.models import Institute,Teacher,Student
# Create your models here.
class AddStudentInst(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    institute = models.ForeignKey(Institute,on_delete=models.CASCADE,null=True,related_name='AddStudentInst')
    courseName = models.CharField(max_length=100,default="")
    forclass = models.CharField(max_length=255,default="")
    teachType = models.CharField(max_length=255,default="")
    batch = models.CharField(max_length=30,default="")
    feeDisc = models.DecimalField(max_digits=10,decimal_places=3,default=0,null=True)
    installments = models.IntegerField(default=2,null=True)
    archieved = models.BooleanField(default=False)  




class School(models.Model):
    name = models.CharField(max_length=150,default="")
    def __str__(self):
        return self.name


class PostTution(models.Model):
    student = models.ForeignKey(Student,on_delete=models.SET_NULL,null=True,related_name='PostTution')
    sno = models.AutoField(primary_key=True)
    subject = models.CharField(max_length=255,default="")
    forclass = models.CharField(max_length=255,default="")
    teachingMode = models.CharField(max_length=255,default="")
    genderPreference = models.CharField(max_length=10,default="",help_text='Female/Male')
    whenToStart = models.CharField(max_length=255,default="")
    description = models.CharField(max_length=1024,default="")
    budget = models.CharField(max_length=10,default="",help_text='Hourly/Monthly')
    budgetVal = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    numberOfSessions = models.DecimalField(max_digits=4,decimal_places=0,default=0)
    assigned = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)


def assignmentDescriptionFiles(instance,filename):
    ext = filename.split('.')[-1]
    return f'assignmentDescriptionFiles/{instance.student.id}/{instance.sno}.{ext}'


class PostAssignment(models.Model):
    student = models.ForeignKey(Student,on_delete=models.SET_NULL,null=True,related_name='PostAssignment')
    sno = models.AutoField(primary_key=True)
    courseName = models.CharField(max_length=255,default="")
    forclass = models.CharField(max_length=255,default="")
    description = models.CharField(max_length=1024,default="")
    descriptionFile = models.FileField(upload_to=assignmentDescriptionFiles,null=True,blank=True)
    deadline = models.DateField(null=True,blank=True)
    budget = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    assigned = models.BooleanField(default=False)
