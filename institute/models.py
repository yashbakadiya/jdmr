from django.db import models
from accounts.models import Institute,Student
# Create your models here.

class InstituteRatings(models.Model):
    institute = models.ForeignKey(Institute,related_name="Coachingreviews",on_delete=models.CASCADE)
    student = models.ForeignKey(Student,related_name="studentenrolledinstitute",on_delete=models.CASCADE)
    Posted_On = models.DateField(auto_now_add=True)
    Review = models.TextField()
    Rating = models.PositiveIntegerField()

    @property
    def Range(self):
        return list(range(self.Rating))

    class Meta:
        ordering = ['-Posted_On']
