from django.db import models

# Create your models here.
         


    

class Voucher(models.Model):
    coupon_code = models.CharField(max_length=20)
    validity = models.DateField()
    amount = models.DecimalField(max_digits=8, decimal_places=2)

class Register(models.Model):
    registerid = models.CharField(max_length=80)
    full_name = models.CharField(max_length=80)
    email = models.EmailField(max_length=254)
    phone_num = models.CharField(max_length=15)
    college_name = models.CharField(max_length=80)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    voucher = models.ForeignKey(Voucher, on_delete=models.CASCADE, null=True)


    # currency = models.CharField(max_length=50)
    # respmsg = models.TextField()
    # bankname = models.CharField(max_length=100)
    # paymentmode = models.CharField(max_length=100)
    # mid = models.CharField(max_length=100)
    # respcode = models.CharField(max_length=50)
    # txnid = models.CharField(max_length=200)
    # banktxnid = models.CharField(max_length=100)