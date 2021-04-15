from django.db import models
from courses.models import Courses
from accounts.models import Student,Teacher,Institute
from django.utils.timezone import now
from datetime import datetime
# Create your models here.
class TutorialInstitute(models.Model):
    Title = models.CharField(max_length=1000)
    Course = models.ForeignKey(Courses,related_name='tutorialsinstitute',on_delete=models.CASCADE)
    forclass = models.CharField(max_length=150, default="")
    Fees = models.PositiveIntegerField()
    Duration = models.PositiveIntegerField()
    Description = models.TextField()
    Validity = models.DateTimeField(null=True, blank=True)
    Discount = models.DecimalField(max_digits=10,decimal_places=6,default=0)
    Archived = models.BooleanField(default=False)
    freeEnrolled = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.Title} {self.Course.courseName}"

    @property
    def Discount_Validity(self):
        if self.Validity:
            if now() <= self.Validity:
                return True

    @property
    def Discounted_price(self):
        return int(self.Fees - (self.Fees*self.Discount)/100)

    @property
    def Off(self):
        return int(self.Discount * 100)

    @property
    def First(self):
        if TutorialInstitutePlaylist.objects.filter(tutorial=TutorialInstitute.objects.get(id=self.id)).exists():
            first = TutorialInstitutePlaylist.objects.filter(tutorial=TutorialInstitute.objects.get(id=self.id)).first()
            return first.Video.url


class TutorialInstitutePlaylist(models.Model):
    tutorial = models.ForeignKey(TutorialInstitute,related_name='playlist',on_delete=models.CASCADE)
    Title = models.CharField(max_length = 1000)
    Description = models.TextField()
    date = models.DateTimeField(default=datetime.now, blank=True)
    Video = models.FileField(upload_to="playlists")

    def __str__(self):
        return self.Title

    def Clip_Duration(self):
        clip = 3
        return clip

class TutorialTutors(models.Model):
    Title = models.CharField(max_length=1000)
    Tutor = models.ForeignKey(Teacher,related_name='tutorialstutor',on_delete=models.CASCADE)
    Course = models.CharField(max_length=150, default="")
    forclass = models.CharField(max_length=150, default="")
    Fees = models.PositiveIntegerField()
    Duration = models.PositiveIntegerField()
    Description = models.TextField()
    Validity = models.DateTimeField(null=True, blank=True)
    Discount = models.DecimalField(max_digits=10,decimal_places=6,default=0)
    Archived = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.Title} {self.Tutor.user.username}"

    @property
    def Discount_Validity(self):
        if self.Validity:
            if now() <= self.Validity:
                return True

    @property
    def Discounted_price(self):
        return int(self.Fees - (self.Fees*self.Discount)/100)

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
    date = models.DateTimeField(default=datetime.now, blank=True)
    Video = models.FileField(upload_to="playlists")

    def __str__(self):
        return self.Title

    def Clip_Duration(self):
        clip = 3
        return clip