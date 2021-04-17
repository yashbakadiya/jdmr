from django.db import models
from django.contrib.auth.models import User
# Create your models here.


def ccImage(instance, filename):
    ext = filename.split('.')[-1]
    return f'profilePics/cc_{instance.user.username}_{instance.id}.{ext}'

# _-----------------------------Abstract Class(This class does not affects database)---------------------


class UsersCommanFields(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    phone = models.CharField(max_length=10, default="1234567899")
    address = models.CharField(max_length=200, blank=True)
   # photo = models.ImageField(upload_to=ccImage, null=True, blank=True)
    photo = models.ImageField(default='default-man.png', upload_to ='users/', null=True, blank=True)
    emailValidated = models.BooleanField(blank=True, default=False)
    phoneValidated = models.BooleanField(blank=True, default=False)
    pincode = models.CharField(max_length=6, default="000000")

    class Meta:
        abstract = True


# ------------------------------------Institute Singup Model---------------------------------------------
class Institute(UsersCommanFields):
    latitude = models.CharField(max_length=20, default="0")
    longitude = models.CharField(max_length=20, default="0")

    def __str__(self):
        return self.user.username


# ------------------------------------Teacher Singup Model-----------------------------------------------
class Teacher(UsersCommanFields):
    dob = models.DateField(blank=True, default="2020-12-1")
    experiance = models.IntegerField(default=-1)
    qualification = models.CharField(max_length=100, default="None")
    desc = models.TextField(default="None")
    democlass = models.BooleanField(default=False)
    forclass = models.TextField(default="None")
    course = models.TextField(default="None")
    teachType = models.TextField(default="None")
    fees = models.TextField(default="None")
    gender = models.CharField(max_length=6, default="Male")

    def __str__(self):
        return self.user.username


# ------------------------------------Student Singup Model-----------------------------------------------
class Student(UsersCommanFields):
    schoolName = models.CharField(max_length=150, default=" ")
    dob = models.DateField(blank=True, default="2020-12-1")

    def __str__(self):
        return self.user.username

###################################teacherID###########
class Tutorid(models.Model):
    teacherid = models.IntegerField(default="0")  
    teachername = models.CharField(max_length=100, default="None")  
    panaadhar = models.CharField(max_length=6, default ="None")
    panaadharnumber = models.CharField(max_length=18,default="None")
    photoid = models.ImageField(upload_to="photoID/",null=True, blank=True)
    def __str__(self):
        return self.teachername
    
   

   