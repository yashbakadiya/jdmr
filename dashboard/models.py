from django.db import models
from accounts.models import Institute,Teacher

# Create your models here.
class OTP(models.Model):
    otp = models.CharField(max_length = 100, primary_key=True)
    user = models.CharField(max_length = 100)
    type = models.CharField(max_length = 100)
    createdAt   = models.DateTimeField(auto_now_add=True)

class tutorPayment (models.Model):
    tutor = models.ForeignKey(Teacher,related_name='tutorpayment',on_delete=models.CASCADE)
    feeCategory = models.TextChoices('feec','Select Premium Diamond')
    feeCategory = models.CharField(default='Select' , max_length=20, choices=feeCategory.choices)
    fee_amt = models.IntegerField(default=0)
    feeCycle = models.CharField(max_length=255, default="", null=True)
    feeDisc = models.DecimalField(max_digits=10, decimal_places=6, default=0)
    discValidity = models.DateTimeField(null=True, blank=True) 
    coupon = models.CharField(max_length=8)
    coupValidity = models.DateTimeField(null=True, blank=True)
    feesstatus = models.CharField(max_length=10, default="Deactive", null=True)
    
    def _str_(self):
        return self.fesstatus

class institutePayment (models.Model):
    institute = models.ForeignKey(Institute,related_name='institutepayment',on_delete=models.CASCADE)
    feeCategory = models.TextChoices('feec','Select Premium Diamond')
    feeCategory = models.CharField(default='Select' , max_length=20, choices=feeCategory.choices)
    fee_amt = models.IntegerField(default=0)
    feeCycle = models.CharField(max_length=255, default="", null=True)
    feeDisc = models.DecimalField(max_digits=10, decimal_places=6, default=0)
    discValidity = models.DateTimeField(null=True, blank=True) 
    coupon = models.CharField(max_length=8)
    coupValidity = models.DateTimeField(null=True, blank=True)
    feesstatus = models.CharField(max_length=10, default="Deactive", null=True)
    
    def _str_(self):
        return self.feesstatus

class TutorTransaction(models.Model):
    gatewayname = models.CharField(max_length=200)
    userid = models.CharField(max_length=80)
    txndate = models.CharField(max_length=80)        
    feeCategory = models.CharField(max_length=255)
    txnamount = models.CharField(max_length=50)
    txnexpdate = models.CharField(max_length=80)        
    status = models.CharField(max_length=80)

class InstituteTransaction(models.Model):
    gatewayname = models.CharField(max_length=200)
    userid = models.CharField(max_length=80)
    txndate = models.CharField(max_length=80)        
    feeCategory = models.CharField(max_length=255)
    txnamount = models.CharField(max_length=50)
    txnexpdate = models.CharField(max_length=80)        
    status = models.CharField(max_length=80)    

    