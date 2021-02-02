from django.db import models

# Create your models here.
class OTP(models.Model):
    otp = models.CharField(max_length = 100, primary_key=True)
    user = models.CharField(max_length = 100)
    type = models.CharField(max_length = 100)
    createdAt   = models.DateTimeField(auto_now_add=True)