import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from tutorSearch.settings import EMAIL_HOST_USER, MERCHANT_KEY, MID
from django.conf import settings
from .models import Register
import razorpay

# For Paytm and Razorpay
KEY_ID = settings.KEY_ID
KEY_SECRET = settings.KEY_SECRET
MID = settings.MID
MERCHANT_KEY = settings.MERCHANT_KEY


def main(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    else:
        return redirect('home')
# Create your views here.

def Razorpay(request):
    if request.is_ajax():
        print("ajax call")
        fullname = request.POST.get('name')
        email = request.POST.get('email')
        phonenum = request.POST.get('phone')
        collegename = request.POST.get('college')
        course = request.POST.get('course')
        amount = request.POST.get('amount')

        register = Register(full_name=fullname, email=email,
                            phone_num=phonenum,
                            college_name=collegename, course=course, amount=amount)
        register.save()

        currentid = register.id

        x = "MS"
        y = str(currentid + 10000)
        z = x+y

        registerobj = Register.objects.get(id=currentid)
        registerobj.registerid = z
        registerobj.save()
        # razorpay integration

        # step 1: Order id

        order_amount = registerobj.amount*100
        order_currency = 'INR'
        client = razorpay.Client(auth=(KEY_ID, KEY_SECRET))
        payment = client.order.create(
            amount=order_amount, currency=order_currency, payment_capture=1)  # return order_id
        print(payment)
        return JsonResponse({'payment_id': payment.id})


