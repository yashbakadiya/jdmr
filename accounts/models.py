from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser, BaseUserManager
# Create your models here.


class MyAccountManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=self.normalize_email(email),
        )
        
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(verbose_name="username", max_length=60, unique=True, blank=True)
    first_name = models.CharField(verbose_name="first name", default='NULL', max_length=60)
    last_name = models.CharField(verbose_name="first name", default='NULL', max_length=60)
    phone_num = models.CharField(verbose_name="phone number", max_length=15)
    user_type = models.CharField(max_length=63, blank=True, null=True)
    date_joined = models.DateTimeField(
        verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    objects = MyAccountManager()

    def __str__(self):
        return self.email

        # For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
        return self.is_admin

        # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True


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
        return self.user.email


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
        return self.user.email


# ------------------------------------Student Singup Model-----------------------------------------------
class Student(UsersCommanFields):
    schoolName = models.CharField(max_length=150, default=" ")
    dob = models.DateField(blank=True, default="2020-12-1")

    def __str__(self):
        return self.user.email

###################################teacherID###########
class Tutorid(models.Model):
    teacherid = models.IntegerField(default="0")  
    teachername = models.CharField(max_length=100, default="None")  
    panaadhar = models.CharField(max_length=6, default ="None")
    panaadharnumber = models.CharField(max_length=18,default="None")
    photoid = models.ImageField(upload_to="photoID/",null=True, blank=True)
    def __str__(self):
        return self.teachername
    
   

   