from django.db import models
from courses.models import Courses
from django.utils.timezone import now
from accounts.models import Institute, Student, Teacher
# Create your models here.


class AddFeesC(models.Model):
    course = models.ForeignKey(
        Courses, on_delete=models.CASCADE, related_name='AddFeesC')
    intitute = models.ForeignKey(Institute, on_delete=models.CASCADE)
    courseName = models.CharField(max_length=100, default="")
    forclass = models.CharField(max_length=255, default="")
    teachType = models.CharField(max_length=255, default="")
    duration = models.CharField(max_length=255, default="")
    fee_amt = models.CharField(max_length=100, default="")
    tax = models.CharField(max_length=100, default="")
    final_amt = models.CharField(max_length=100, default="")
    no_of_installment = models.CharField(max_length=100, default="")
    typeOfCharge = models.DecimalField(
        max_digits=1, decimal_places=0, help_text='0-> percent || 1-> amount || else-> error')
    extra_charge = models.CharField(max_length=255, default="")
    feeDisc = models.DecimalField(max_digits=10, decimal_places=6, default=0)
    discValidity = models.DateTimeField(default=now)
    final_amount = models.DecimalField(max_digits=10, decimal_places=2)
    archieved = models.BooleanField(default=False)

    def __str__(self):
        return self.course.courseName + " ," + str(self.fee_amt)


class SubmitFees(models.Model):
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name='fees')
    fees = models.ForeignKey(AddFeesC, on_delete=models.CASCADE,related_name="stu_fees",default="")
    totalFee = models.DecimalField(max_digits=10, decimal_places=2)
    feePayed = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    balanceFee = models.DecimalField(max_digits=10, decimal_places=2)
    instalmentDue = models.DecimalField(max_digits=10, decimal_places=2)
    totalInstallments = models.DecimalField(max_digits=10, decimal_places=2)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)


class Instalment(models.Model):
    feeObj = models.ForeignKey(
        "SubmitFees", on_delete=models.CASCADE, related_name='Instalment')
    instalmentNum = models.DecimalField(max_digits=3, decimal_places=0)
    paymentExp = models.DecimalField(max_digits=10, decimal_places=2)
    paymentDone = models.DecimalField(max_digits=10, decimal_places=2)
    timeStamp = models.DateTimeField(auto_now_add=True)
