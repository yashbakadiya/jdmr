from django.db import models
from courses.models import Courses
from django.utils.timezone import now
from accounts.models import Institute, Student, Teacher
from students.models import AddStudentInst
# Create your models here.


class AddFeesC(models.Model):
    course = models.ForeignKey(
        Courses, on_delete=models.CASCADE, related_name='AddFeesC',null=True )
    intitute = models.ForeignKey(Institute, on_delete=models.CASCADE,null=True )
    courseName = models.CharField(max_length=100, default="",null=True )
    forclass = models.CharField(max_length=255, default="",null=True )
    teachType = models.CharField(max_length=255, default="",null=True )
    duration = models.CharField(max_length=255, default="",null=True)
    fee_amt = models.CharField(max_length=100, default="",null=True )
    tax = models.CharField(max_length=100, default="",null=True )
    final_amt = models.CharField(max_length=100, default="",null=True )
    no_of_installment = models.CharField(max_length=100, default="",null=True )
    typeOfCharge = models.DecimalField(
        max_digits=1, decimal_places=0, help_text='0-> percent || 1-> amount || else-> error')
    extra_charge = models.CharField(max_length=255, default="")
    feeDisc = models.DecimalField(max_digits=10, decimal_places=6, default=0)
    discValidity = models.DateTimeField(null=True,blank=True)
    final_amount = models.DecimalField(max_digits=10, decimal_places=2)
    feesstatus = models.CharField(max_length=10, default="Un paid",null=True)
    archieved = models.BooleanField(default=False)
    def __str__(self):
        return self.course.courseName +" "+ str(self.fee_amt) +" "+self.forclass       




class SubmitFees(models.Model):
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name='fees')
    fees = models.ForeignKey(AddFeesC, on_delete=models.CASCADE,related_name="stu_fees",default="",null=True )
    totalFee = models.DecimalField(max_digits=10, decimal_places=2,null=True )
    feePayed = models.DecimalField(max_digits=10, decimal_places=2, default=0,null=True )
    instalmentDue = models.DecimalField(max_digits=10, decimal_places=2,null=True, default=1 )
    totalInstallments = models.DecimalField(max_digits=10, decimal_places=2,null=True )
    feesstatus = models.CharField(max_length=10, default="Un paid",null=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)


class Instalment(models.Model):
    feeObj = models.ForeignKey(
        "SubmitFees", on_delete=models.CASCADE, related_name='Instalment')
    instalmentNum = models.DecimalField(max_digits=3, decimal_places=0)
    paymentExp = models.DecimalField(max_digits=10, decimal_places=2)
    paymentDone = models.DecimalField(max_digits=10, decimal_places=2)
    timeStamp = models.DateTimeField(auto_now_add=True)




    
