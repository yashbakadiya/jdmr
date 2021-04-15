from django.db import models
from accounts.models import Institute,Student,Teacher
from courses.models import TeachingType
from secrets import token_urlsafe
# Create your models here.

class enrollTutors(models.Model):
    institute = models.ForeignKey(Institute,on_delete=models.CASCADE)
    courseName = models.CharField(max_length=100,default="")
    forclass = models.CharField(max_length=255,default="")
    teachType = models.CharField(max_length=255,default="")
    teacher = models.ForeignKey(Teacher,on_delete=models.CASCADE)
    availability = models.CharField(max_length=30)
    archieved = models.BooleanField(default=False)


class TutorRatings(models.Model):
    Tutor = models.ForeignKey(Teacher,related_name="tutorreviews",on_delete=models.CASCADE)
    Student = models.ForeignKey(Student,related_name="studentenrolledtutor",on_delete=models.CASCADE)
    Posted_On = models.DateField(auto_now_add=True)
    Review = models.TextField()
    Rating = models.PositiveIntegerField()

    @property
    def Range(self):
        return list(range(self.Rating))

    class Meta:
        ordering = ['-Posted_On']


class MakeAppointment(models.Model):
    dateTime        = models.DateTimeField()
    duration        = models.DurationField()
    timezone        = models.CharField(max_length=35,default="")
    recc            = models.BooleanField(help_text='Reccurance')
    pattern         = models.CharField(max_length=2,default="",null=True,help_text='D-Daily/W=Weekly')
    repeat          = models.DecimalField(max_digits=3,null=True,decimal_places=0,default=-1)
    days            = models.CharField(max_length=50,default="",null=True)
    endingDate      = models.DateField(null=True)
    tutor           = models.ForeignKey(Teacher,on_delete=models.SET_NULL,null=True,related_name='MakeAppointment')
    student         = models.ForeignKey(Student,on_delete=models.SET_NULL,null=True,related_name='MakeAppointment')
    daysDump        = models.TextField()
    utcDateTime     = models.DateTimeField()
    utcEndingDate   = models.DateField(null=True)
    accepted        = models.BooleanField(default=False)
    done            = models.BooleanField(default=False)
    rating          = models.DecimalField(max_digits=1,decimal_places=0,default=0)
    sno             = models.AutoField(primary_key=True)
    uid             = models.CharField(max_length=50,default="")
    created_by      = models.BooleanField(default=False, null=True, blank=True)  #False-> by_student, True->by_teacher

    def save(self, *args, **kwargs):
        self.uid = token_urlsafe(50)[:50]
        print(self.uid)
        super(MakeAppointment, self).save(*args, **kwargs)