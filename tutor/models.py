from django.db import models
from django.core.validators import MinLengthValidator
from django.core.validators import MinValueValidator
from django.core.validators import MaxValueValidator
from django.core.validators import MaxLengthValidator
from secrets import token_urlsafe
import json
from django.utils.timezone import now
from moviepy.editor import *

# Create your models here.
class LoginCoachingCentre(models.Model):
    sno = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100,default="")
    password = models.CharField(max_length=20, default="")

def ccImage(instance,filename):
    ext = filename.split('.')[-1]
    return f'profilePics/cc_{instance.instituteCode}_{instance.s_no}.{ext}'

class SignupCoachingCentre(models.Model):
    s_no = models.AutoField(primary_key=True)
    instituteCode = models.CharField(max_length=6,default="")
    instituteName = models.CharField(max_length=100,default="")
    email = models.CharField(max_length=70,validators=[MinLengthValidator(3)],default="")
    password = models.CharField(max_length=20, default="")
    phone = models.CharField(max_length=10,validators=[MinLengthValidator(10)],default="",help_text = "Enter 10 digit phone number")
    location = models.CharField(max_length=255,default="")
    photo = models.ImageField(upload_to=ccImage,null=True,blank=True)
    avatar = models.DecimalField(max_digits=2,decimal_places=0,default=0)
    latitude = models.CharField(max_length=20,default="0")
    longitude = models.CharField(max_length=20,default="0")
    showFees = models.BooleanField(default=True)
    emailValidated = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if(not self.photo and self.avatar==0):
            self.avatar = 21
        super(SignupCoachingCentre, self).save(*args, **kwargs)

class AddCourses(models.Model):
    s_num = models.AutoField(primary_key=True)
    cid = models.CharField(max_length=5,default="")
    courseName = models.CharField(max_length=100,default="")
    forclass = models.CharField(max_length=150,default="")
    coachingCentre = models.ForeignKey('SignupCoachingCentre', on_delete=models.CASCADE, related_name='AddCourses')

class ArchiveCourses(models.Model):
    sn = models.AutoField(primary_key=True)
    crid = models.CharField(max_length=5,default="")
    crName = models.CharField(max_length=100,default="")
    crclass = models.CharField(max_length=150,default="")
    coachingCentre = models.ForeignKey('SignupCoachingCentre', on_delete=models.CASCADE, related_name='ArchiveCourses')

class TeachingType(models.Model):
    s_num = models.AutoField(primary_key=True)
    course = models.ForeignKey('AddCourses', on_delete=models.CASCADE, related_name='TeachingType')
    courseName = models.CharField(max_length=100,default="")
    forclass = models.CharField(max_length=255,default="")
    teachType = models.CharField(max_length=255,default="")
    duration = models.CharField(max_length=255,default="")
    timePeriod = models.CharField(max_length=255,default="")

class ViewTeachingType(models.Model):
    s_num = models.AutoField(primary_key=True)
    cid = models.CharField(max_length=5,default="")
    courseName = models.CharField(max_length=100,default="")
    forclass = models.CharField(max_length=255,default="")
    teachType = models.CharField(max_length=255,default="")
    durationInMonths = models.CharField(max_length=255,default="")

class SignupTutor(models.Model):
    sno = models.AutoField(primary_key=True)
    tutorCode = models.CharField(max_length=6,default="")
    username = models.CharField(max_length=100,default="")
    firstName = models.CharField(max_length=100,default="")
    lastName = models.CharField(max_length=100,default="")
    email = models.CharField(max_length=70,validators=[MinLengthValidator(3)],default="")
    password = models.CharField(max_length=20, default="")
    distance = models.PositiveIntegerField(validators=[MaxValueValidator(99999)],default=0)
    location = models.CharField(max_length=255,default="")
    phone = models.CharField(max_length=10,validators=[MinLengthValidator(10)],default="",help_text = "Enter 10 digit phone number")
    latitude = models.CharField(max_length=20,default="0")
    longitude = models.CharField(max_length=20,default="0")
    emailValidated = models.BooleanField(default=False)


def userImagePath(instance,filename):
    ext = filename.split('.')[-1]
    return f'profilePics/user_{instance.base.tutorCode}_{instance.base.sno}_{instance.sno}.{ext}'

class SignupTutorContinued(models.Model):
    sno = models.AutoField(primary_key=True)
    base = models.ForeignKey('SignupTutor',on_delete=models.CASCADE,null=True,related_name='signupTutorContinued')
    availability = models.CharField(max_length=255,default="")
    qualification = models.CharField(max_length=255,default="")
    experience = models.DecimalField(max_digits=5,decimal_places=1,default=0)
    description = models.CharField(max_length=1024,default="")
    gender = models.CharField(max_length=10,default="",help_text='Female/Male')
    courseName = models.CharField(max_length=255,default="",null=True)
    forclass = models.CharField(max_length=255,default="",null=True)
    fees = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    photo = models.ImageField(upload_to=userImagePath,null=True,blank=True)
    freeDemo = models.DecimalField(max_digits=1,decimal_places=0,default=0)
    avatar = models.DecimalField(max_digits=2,decimal_places=0,default=0)
    def save(self, *args, **kwargs):
        if(not self.photo and self.avatar==0):
            if(self.gender=='Male'):
                self.avatar = 2
            elif(self.gender=='Female'):
                self.avatar = 1
            else:
                self.avatar = 0
        super(SignupTutorContinued, self).save(*args, **kwargs)

class ArchiveTutors(models.Model):
    sno = models.AutoField(primary_key=True)
    tutorCode = models.CharField(max_length=6,default="")
    username = models.CharField(max_length=100,default="")
    firstName = models.CharField(max_length=100,default="")
    lastName = models.CharField(max_length=100,default="")
    email = models.CharField(max_length=70,validators=[MinLengthValidator(3)],default="")
    password = models.CharField(max_length=20, default="")
    distance = models.PositiveIntegerField(validators=[MaxValueValidator(99999)],default=0)
    location = models.CharField(max_length=255,default="")
    phone = models.CharField(max_length=10,validators=[MinLengthValidator(10)],default="",help_text = "Enter 10 digit phone number")
    latitude = models.CharField(max_length=20,default="0")
    longitude = models.CharField(max_length=20,default="0")
    availability = models.CharField(max_length=255,default="")
    qualification = models.CharField(max_length=255,default="")
    experience = models.DecimalField(max_digits=5,decimal_places=1,default=0)
    description = models.CharField(max_length=1024,default="")
    gender = models.CharField(max_length=10,default="",help_text='Female/Male')
    courseName = models.CharField(max_length=255,default="",null=True)
    forclass = models.CharField(max_length=255,default="",null=True)
    fees = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    photo = models.ImageField(upload_to=userImagePath,null=True,blank=True)
    freeDemo = models.DecimalField(max_digits=1,decimal_places=0,default=0)
    avatar = models.DecimalField(max_digits=2,decimal_places=0,default=0)
    teachType = models.CharField(max_length=255,default="")
    instituteName = models.CharField(max_length=255,default="")
    instituteCode = models.CharField(max_length=255,default="")

def assignmentDescriptionFiles(instance,filename):
    ext = filename.split('.')[-1]
    return f'assignmentDescriptionFiles/{instance.connector.snum}/{instance.sno}.{ext}'

class PostAssignment(models.Model):
    connector = models.ForeignKey('SignupStudent',on_delete=models.SET_NULL,null=True,related_name='PostAssignment')
    sno = models.AutoField(primary_key=True)
    courseName = models.CharField(max_length=255,default="")
    forclass = models.CharField(max_length=255,default="")
    description = models.CharField(max_length=1024,default="")
    descriptionFile = models.FileField(upload_to=assignmentDescriptionFiles,null=True,blank=True)
    requirement = models.DecimalField(max_digits=4,decimal_places=0)
    budget = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    assigned = models.BooleanField(default=False)

class PostTution(models.Model):
    connector = models.ForeignKey('SignupStudent',on_delete=models.SET_NULL,null=True,related_name='PostTution')
    sno = models.AutoField(primary_key=True)
    courseName = models.CharField(max_length=255,default="")
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


# class AddTutors(models.Model):
#     sno = models.AutoField(primary_key=True)
#     tutorname = models.CharField(max_length=100,default="")
#     email = models.CharField(max_length=70,validators=[MinLengthValidator(3)],default="")
#     password = models.CharField(max_length=20, default="")
#     phone = models.CharField(max_length=10,validators=[MinLengthValidator(10)],default="",help_text = "Enter 10 digit phone number")
#     instituteName = models.CharField(max_length=255,default="")
#     courseTaught = models.CharField(max_length=100,default="")
#     forclass = models.CharField(max_length=50,default="")
#     availability = models.CharField(max_length=50,default="")
#     teachType = models.CharField(max_length=50,default="")

class AddTutorsInst(models.Model):
    username = models.ForeignKey('enrollTutors',on_delete=models.CASCADE,null=True,related_name='AddTutorsInst')
    cid = models.ForeignKey('SignupCoachingCentre',on_delete=models.SET_NULL,null=True,related_name='tutor_cid',related_query_name='tutor_cid')
    courseTaught = models.CharField(max_length=100,default="")
    forclass = models.CharField(max_length=255,default="")
    teachType = models.CharField(max_length=255,default="")
    availability = models.DecimalField(max_digits=1,decimal_places=0,default=0,help_text='0=>nothing,1=>weekly,2=>weekend,3=>both')

class enrollTutors(models.Model):
    sno = models.AutoField(primary_key=True)
    signUp = models.ForeignKey('SignupTutor',on_delete=models.CASCADE ,null=True,related_name='enrollTutors')
    instituteName = models.CharField(max_length=255,default="")
    instituteCode = models.CharField(max_length=255,default="")


def studentImagePath(instance,filename):
    ext = filename.split('.')[-1]
    return f'profilePics/student_{instance.studentCode}_{instance.username}.{ext}'

class SignupStudent(models.Model):
    snum = models.AutoField(primary_key=True)
    studentCode = models.CharField(max_length=6,default="")
    username = models.CharField(max_length=100,default="")
    firstName = models.CharField(max_length=100,default="")
    lastName = models.CharField(max_length=100,default="")
    email = models.CharField(max_length=100,default="")
    password = models.CharField(max_length=20, default="")
    phone = models.CharField(max_length=10,validators=[MinLengthValidator(10)],default="",help_text = "Enter 10 digit phone number")
    location = models.CharField(max_length=255,default="")
    photo = models.ImageField(upload_to=studentImagePath,null=True,blank=True)
    schoolName = models.CharField(max_length=100,default="")
    avatar = models.DecimalField(max_digits=2,decimal_places=0,default=0)
    latitude = models.CharField(max_length=20,default="0")
    longitude = models.CharField(max_length=20,default="0")
    emailValidated = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if(not self.photo and self.avatar==0):
            self.avatar = 20
        super(SignupStudent, self).save(*args, **kwargs)

    @property
    def Full_name(self):
        return f"{self.firstName} {self.lastName}"

class AddStudentInst(models.Model):
    snum = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100,default="")
    conector = models.ForeignKey('SignupStudent',on_delete=models.CASCADE,null=True,related_name='AddStudentInst')
    instituteName = models.CharField(max_length=255,default="")
    instituteCode = models.CharField(max_length=255,default="")

class AddStudentDetail(models.Model):
    snum = models.AutoField(primary_key=True)
    username = models.ForeignKey('AddStudentInst',on_delete=models.CASCADE,null=True,related_name='AddStudentDetail',related_query_name='AddStudentDetail')
    courseName = models.CharField(max_length=255,default="")
    teachType = models.CharField(max_length=255,default="")
    forclass = models.CharField(max_length=255,default="")
    batch = models.CharField(max_length=255,default="")
    instalment = models.DecimalField(max_digits=2,decimal_places=0,default=1)
    feeDisc = models.DecimalField(max_digits=10,decimal_places=2,null=True,default=0)

class ArchiveStudents(models.Model):
    snum = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100,default="")
    conector = models.ForeignKey('SignupStudent',on_delete=models.CASCADE,null=True,related_name='ArchiveStudents')
    instituteName = models.CharField(max_length=255,default="")
    instituteCode = models.CharField(max_length=255,default="")
    addStudentDetail = models.ForeignKey('AddStudentDetail',on_delete=models.SET_NULL,null=True,related_name='ArchiveStudents')

class AddFees(models.Model):
    sno = models.AutoField(primary_key=True)
    courseName = models.CharField(max_length=100,default="")
    teachType = models.CharField(max_length=100, default="")
    duration = models.CharField(max_length=100, default="")
    feeDuration = models.CharField(max_length=100, default="")
    no_of_installment = models.CharField(max_length=100,default="")
    feeamt = models.CharField(max_length=100,default="")

class AddFeesC(models.Model):
    sno = models.AutoField(primary_key=True)
    course = models.ForeignKey(AddCourses,on_delete=models.CASCADE,related_name='AddFeesC')
    courseName = models.CharField(max_length=100,default="")
    forclass = models.CharField(max_length=255,default="")
    teachType = models.CharField(max_length=255, default="")
    duration = models.CharField(max_length=255, default="")
    fee_amt = models.CharField(max_length=100,default="")
    tax = models.CharField(max_length=100,default="")
    final_amt = models.CharField(max_length=100,default="")
    no_of_installment = models.CharField(max_length=100,default="")
    typeOfCharge = models.DecimalField(max_digits=1,decimal_places=0,help_text='0-> percent || 1-> amount || else-> error')
    extra_charge = models.CharField(max_length=255,default="")
    feeDisc = models.DecimalField(max_digits=10,decimal_places=6,default=0)
    discValidity = models.DateTimeField(default=now)
    final_amount =  models.DecimalField(max_digits=10,decimal_places=6)

class ArchiveFees(models.Model):
    sno = models.AutoField(primary_key=True)
    course = models.OneToOneField(AddCourses,on_delete=models.CASCADE,related_name='ArchiveFees')
    courseName = models.CharField(max_length=100,default="")
    forclass = models.CharField(max_length=255,default="")
    teachType = models.CharField(max_length=255, default="")
    duration = models.CharField(max_length=255, default="")
    fee_amt = models.CharField(max_length=100,default="")
    tax = models.CharField(max_length=100,default="")
    final_amt = models.CharField(max_length=100,default="")
    no_of_installment = models.CharField(max_length=100,default="")
    typeOfCharge = models.DecimalField(max_digits=1,decimal_places=0,help_text='0-> percent || 1-> amount || else-> error')
    extra_charge = models.CharField(max_length=255,default="")
    final_amount =  models.DecimalField(max_digits=10,decimal_places=6)

class School(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class SubmitFees(models.Model):
    sno         = models.AutoField(primary_key=True)
    username    = models.ForeignKey("AddStudentDetail",on_delete=models.CASCADE,related_name='fees')
    subject     = models.CharField(max_length=255,default="")
    totalFee    = models.DecimalField(max_digits=10,decimal_places=2)
    feePayed    = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    balanceFee  = models.DecimalField(max_digits=10,decimal_places=2)
    instalmentDue = models.DecimalField(max_digits=10,decimal_places=2)
    totalInstallments = models.DecimalField(max_digits=10,decimal_places=2)
    createdAt   = models.DateTimeField(auto_now_add=True)
    updatedAt   = models.DateTimeField(auto_now=True)

class Instalment(models.Model):
    sno             = models.AutoField(primary_key=True)
    feeObj          = models.ForeignKey("SubmitFees",on_delete=models.CASCADE,related_name='Instalment')
    instalmentNum   = models.DecimalField(max_digits=3,decimal_places=0)
    paymentExp      = models.DecimalField(max_digits=10,decimal_places=2)
    paymentDone     = models.DecimalField(max_digits=10,decimal_places=2)
    timeStamp       = models.DateTimeField(auto_now_add=True)

class BatchTiming(models.Model):
    sno             = models.AutoField(primary_key=True)
    batchName       = models.CharField(max_length=255,default="")
    days            = models.CharField(max_length=255,default="",help_text="Comma seperated")
    startTime       = models.CharField(max_length=255,default="")
    endTime         = models.CharField(max_length=255,default="")
    original24time  = models.CharField(max_length=255,default="",help_text="Comma seperated")
    createdAt       = models.DateTimeField(auto_now_add=True)
    updatedAt       = models.DateTimeField(auto_now=True)
    coachingCenter  = models.ForeignKey('SignupCoachingCentre',on_delete=models.SET_NULL,null=True,related_name='BatchTiming')

class MakeAppointment(models.Model):
    dateTime        = models.DateTimeField()
    duration        = models.DurationField()
    timezone        = models.CharField(max_length=35,default="")
    recc            = models.BooleanField(help_text='Reccurance')
    pattern         = models.CharField(max_length=2,default="",null=True,help_text='D-Daily/W=Weekly')
    repeat          = models.DecimalField(max_digits=3,null=True,decimal_places=0,default=-1)
    days            = models.CharField(max_length=50,default="",null=True)
    endingDate      = models.DateField(null=True)
    tutor           = models.ForeignKey('SignupTutor',on_delete=models.SET_NULL,null=True,related_name='MakeAppointment')
    student         = models.ForeignKey('SignupStudent',on_delete=models.SET_NULL,null=True,related_name='MakeAppointment')
    daysDump        = models.TextField()

    utcDateTime     = models.DateTimeField()
    utcEndingDate   = models.DateField(null=True)

    accepted        = models.BooleanField(default=False)
    done            = models.BooleanField(default=False)
    rating          = models.DecimalField(max_digits=1,decimal_places=0,default=0)

    sno             = models.AutoField(primary_key=True)
    uid             = models.CharField(max_length=50,default="")

    def save(self, *args, **kwargs):
        self.uid = token_urlsafe(50)
        if(isinstance(self.days,list)):
            self.days = json.dumps(self.days)
            super(MakeAppointment, self).save(*args, **kwargs)
        else:
            raise TypeError(f'Days should a list but is {type(self.days)} - {self.days}')

class temp(models.Model):
    recc            = models.BooleanField()
    def save(self, *args, **kwargs):
        if(self.recc == 'a'):
            self.recc = True
        super(temp, self).save(*args, **kwargs)

class Notice(models.Model):
    sno                 = models.AutoField(primary_key=True)
    title               = models.CharField(max_length=35,default="")
    description         = models.TextField()
    createdAt           = models.DateTimeField(auto_now_add=True)
    batch               = models.ForeignKey('BatchTiming',on_delete=models.CASCADE,null=True,related_name='Notice')


class TutorialInstitute(models.Model):
    Title = models.CharField(max_length=1000)
    Course = models.ForeignKey(AddCourses,related_name='tutorialsinstitute',on_delete=models.CASCADE)
    Fees = models.PositiveIntegerField()
    Duration = models.PositiveIntegerField()
    Description = models.TextField()
    Validity = models.DateTimeField()
    Discount = models.DecimalField(max_digits=10,decimal_places=6,default=0)
    Archived = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.Title} {self.Course.courseName}"

    @property
    def Discount_Validity(self):
        if now() <= self.Validity:
            return True

    @property
    def Discounted_price(self):
        return int(self.Fees - (self.Fees*self.Discount))

    @property
    def Off(self):
        return int(self.Discount * 100)


class TutorialInstitutePlaylist(models.Model):
    tutorial = models.ForeignKey(TutorialInstitute,related_name='playlist',on_delete=models.CASCADE)
    Title = models.CharField(max_length = 1000)
    Description = models.TextField()
    Video = models.FileField(upload_to="playlists")

    def __str__(self):
        return self.Title

    def Clip_Duration(self):
        clip = 3
        return clip

class TutorialTutors(models.Model):
    Title = models.CharField(max_length=1000)
    Tutor = models.ForeignKey(SignupTutor,related_name='tutorialstutor',on_delete=models.CASCADE)
    Fees = models.PositiveIntegerField()
    Duration = models.PositiveIntegerField()
    Description = models.TextField()
    Validity = models.DateTimeField()
    Discount = models.DecimalField(max_digits=10,decimal_places=6,default=0)
    Archived = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.Title} {self.Tutor.username}"

    @property
    def Discount_Validity(self):
        if now() <= self.Validity:
            return True

    @property
    def Discounted_price(self):
        return int(self.Fees - (self.Fees*self.Discount))

    @property
    def Off(self):
        return int(self.Discount * 100)

    @property
    def First(self):
        if TutorialTutorsPlaylist.objects.filter(tutorial=TutorialTutors.objects.get(id=self.id)).exists():
            first = TutorialTutorsPlaylist.objects.filter(tutorial=TutorialTutors.objects.get(id=self.id)).first()
            return first.Video.url
    

class TutorialTutorsPlaylist(models.Model):
    tutorial = models.ForeignKey(TutorialTutors,related_name='tutorplaylist',on_delete=models.CASCADE)
    Title = models.CharField(max_length = 1000)
    Description = models.TextField()
    Video = models.FileField(upload_to="playlists")

    def __str__(self):
        return self.Title

    def Clip_Duration(self):
        clip = 3
        return clip

class OTP(models.Model):
    otp = models.CharField(max_length = 100, primary_key=True)
    user = models.CharField(max_length = 100)
    type = models.CharField(max_length = 100)
    createdAt   = models.DateTimeField(auto_now_add=True)


class ReviewsTutor(models.Model):
    Tutor = models.ForeignKey(TutorialTutors,related_name="Tutorreviews",on_delete=models.CASCADE)
    Student = models.ForeignKey(SignupStudent,related_name="tutorreview",on_delete=models.CASCADE)
    Posted_On = models.DateField(auto_now_add=True)
    Review = models.CharField(max_length=2000)
    Rating = models.PositiveIntegerField()
    
    @property
    def Range(self):
        return list(range(self.Rating))

    class Meta:
        ordering = ['-Posted_On']

class ReviewsInstitute(models.Model):
    Institute = models.ForeignKey(TutorialInstitute,related_name="Institutereviews",on_delete=models.CASCADE)
    Student = models.ForeignKey(SignupStudent,related_name="institutereview",on_delete=models.CASCADE)
    Posted_On = models.DateField(auto_now_add=True)
    Review = models.CharField(max_length=2000)
    Rating = models.PositiveIntegerField()

    @property
    def Range(self):
        return list(range(self.Rating))

    class Meta:
        ordering = ['-Posted_On']