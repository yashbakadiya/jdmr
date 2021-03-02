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
    gender = models.CharField(max_length=6, default="Male")
    forclass = models.CharField(max_length=30, default="None")
    desc = models.TextField(default="None")
    course = models.CharField(max_length=150, default="None")
    qualification = models.CharField(max_length=100, default="None")
    experiance = models.IntegerField(default=-1)
    fees = models.IntegerField(default=1000)
    democlass = models.BooleanField(default=False)
    availability = models.CharField(max_length=30, default="None")

    def __str__(self):
        return self.user.username


# ------------------------------------Student Singup Model-----------------------------------------------
class Student(UsersCommanFields):
    schoolName = models.CharField(max_length=150, default=" ")
    dob = models.DateField(blank=True, default="2020-12-1")

    def __str__(self):
        return self.user.username
