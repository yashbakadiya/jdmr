from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import Institute, Teacher, Student
from .models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework import viewsets
from .serializers import InstituteSerializer, StudentSerializer, TeacherSerializer, UserSerializer

from django.core.mail import EmailMessage

from django.conf import settings


# Create your views here.



# 1---------------------------------------------Login User View------------------------------------------

def forgotpassword(request):
    
    return (render ,"accounst/password-reset/password_reset_form.html")
def login(request):
    errors = []
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        prefil = {
            'username':username,
            'password':password,
            'type':request.POST['type'],
        }

        try:
            user = auth.authenticate(email=username, password=password)
            request.session["user"] = username
            if request.POST['type'] == "Institute":
                i = Institute.objects.get(user=user)
                auth.login(request, user)
                request.session["type"] = request.POST['type']
                return redirect("dashboard")
            elif request.POST['type'] == "Teacher":
                Teacher.objects.get(user=user)
                auth.login(request, user)
                request.session["type"] = request.POST['type']
                return redirect("dashboard")
            elif request.POST['type'] == "Student":
                Student.objects.get(user=user)
                auth.login(request, user)
                request.session["type"] = request.POST['type']
                return redirect("dashboard")
        except:
            errors.append("Invalid Credencials")
            return render(request, "accounts/loginAll.html", {'errors': errors,"prefil": prefil})
    return render(request, "accounts/loginAll.html", {'errors': errors})


# ------------------------------------------------Signup User View---------------------------------------
def signup(request):
    errors = []
    prefil = {}
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        user_type = request.POST['type']
        prefil = {
            'username': username,
            'password': password,
            'email': email,
            'phone': phone,
            'type': request.POST['type']
        }

        try:
            username = User.objects.get(email = email)
            errors.append("Username Already Taken")
            return render(request, "accounts/signup.html", {"errors": errors, "prefil": prefil})
        except:
            user = User(email=email, username=username, password=password)
        try:
            email = User.objects.get(email = email)
            errors.append("Email Already Taken")
            return render(request, "accounts/signup.html", {"errors": errors, "prefil": prefil})
        except:
            user.email=email

        if user_type == "Institute":
            try:
                phone = Institute.objects.get(phone=phone)
                errors.append("Phone Number Already Taken")
                return render(request, "accounts/signup.html", {"errors": errors, "prefil": prefil})
            except:
                user.set_password(password)
                user.save()
                Institute(user=user, phone=phone).save()

        elif user_type == "Teacher":
            try:
                phone = Teacher.objects.get(phone=phone)
                errors.append("Phone Number Already Taken")
                return render(request, "accounts/signup.html", {"errors": errors, "prefil": prefil})
            except:
                user.save()
                Teacher(user=user, phone=phone).save()

        elif user_type == "Student":
            try:
                phone = Student.objects.get(phone=phone)
                errors.append("Phone number Already Taken")
                return render(request, "accounts/signup.html", {"errors": errors, "prefil": prefil})
            except:
                user.save()
                Student(user=user, phone=phone).save()
            
        auth.login(request, user)
        request.session["user"] = username
        request.session["type"] = user_type
        return redirect("dashboard")
    return render(request, 'accounts/signup.html')


@login_required(login_url='Login')
def testing(request):
    return HttpResponse("you login succesfully")


# ------------------------------------------Logout User View---------------------------------------------
@login_required(login_url='Login')
def logout(request):
    request.session.flush()
    auth.logout(request)
    return render(request, "accounts/loginAll.html")
