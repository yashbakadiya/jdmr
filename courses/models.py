from django.db import models
from accounts.models import Institute
# Create your models here.


class Courses(models.Model):
    courseID = models.CharField(max_length=25, default="")
    courseName = models.CharField(max_length=100, default="")
    forclass = models.CharField(max_length=150, default="")
    intitute = models.ForeignKey(
        Institute, on_delete=models.CASCADE, related_name='AddCourses')
    archieved = models.BooleanField(default=False)

    def __str__(self):
     #   return self.courseName+" "+self.forclass
        return str(self.id)+" "+self.courseName + " "+self.forclass


class TeachingType(models.Model):
    course = models.ForeignKey(
        'Courses', on_delete=models.CASCADE, related_name='TeachingType')
    courseID = models.IntegerField(default=None)
    forclass = models.CharField(max_length=255, default="")
    teachType = models.CharField(max_length=255, default="")
    duration = models.CharField(max_length=255, default="")
    timePeriod = models.CharField(max_length=255, default="")

    def __str__(self):
        return self.course.courseName+" "+self.course.forclass+" "+self.teachType
