from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import Institute, Teacher, Student
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework import viewsets
from .serializers import InstituteSerializer, StudentSerializer, TeacherSerializer, UserSerializer


# Create your views here.



# 1---------------------------------------------Login User View------------------------------------------


def login(request):
    errors = []
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username, password=password)
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
            return render(request, "accounts/loginAll.html", {'errors': errors})
    return render(request, "accounts/loginAll.html", {'errors': errors})


# ------------------------------------------------Signup User View---------------------------------------
def signup(request):
    errors = []
    prefil = {}
    if request.method == "POST":
        username = request.POST.get('username')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        password = request.POST.get('password')
        confpassword = request.POST.get('confpassword')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        user_type = request.POST['type']
        prefil = {
            'username': username,
            'firstname': firstname,
            'lastname': lastname,
            'password': password,
            'confpassword': confpassword,
            'email': email,
            'phone': phone,
            'address': address
        }
        if password != confpassword:
            errors.append("Passwords do not match")
            return render(request, "accounts/signup.html", {"errors": errors, "prefil": prefil})
        if user_type == "Institute":
            try:
                email = Institute.objects.get(user__email=email)
                errors.append("Email Already Taken")
                return render(request, "accounts/signup.html", {"errors": errors, "prefil": prefil})
            except:
                email = request.POST.get('email')
            try:
                phone = Institute.objects.get(phone=phone)
                errors.append("phone number Already Taken")
                return render(request, "accounts/signup.html", {"errors": errors, "prefil": prefil})
            except:
                phone = request.POST.get('phone')
            try:
                username = Institute.objects.get(user__username=username)
                errors.append("Name Already Taken")
                return render(request, "accounts/signup.html", {"errors": errors, "prefil": prefil})
            except:
                username = request.POST.get('username')
            user = User(username=username, first_name=firstname,
                        last_name=lastname, password=password, email=email)
            user.save()
            Institute(user=user, address=address, phone=phone).save()
            auth.login(request, user)
            request.session["user"] = username
            request.session["type"] = request.POST['type']
            return redirect("dashboard")
        elif user_type == "Teacher":
            try:
                email = Teacher.objects.get(user__email=email)
                errors.append("Email Already Taken")
                return render(request, "accounts/signup.html", {"errors": errors, "prefil": prefil})
            except:
                email = request.POST.get('email')
            try:
                phone = Teacher.objects.get(phone=phone)
                errors.append("Phone number Already Taken")
                return render(request, "accounts/signup.html", {"errors": errors, "prefil": prefil})
            except:
                phone = request.POST.get('phone')
            try:
                username = Teacher.objects.get(user__username=username)
                errors.append("Name Already Taken")
                return render(request, "accounts/signup.html", {"errors": errors, "prefil": prefil})
            except:
                username = request.POST.get('username')
            user = User(username=username, first_name=firstname,
                        last_name=lastname, password=password, email=email)
            user.save()
            Teacher(user=user, address=address, phone=phone).save()
            auth.login(request, user)
            request.session["user"] = username
            request.session["type"] = request.POST['type']
            return redirect("dashboard")

        elif user_type == "Student":
            try:
                email = Student.objects.get(user__email=email)
                errors.append("Email Already Taken")
                return render(request, "accounts/signup.html", {"errors": errors, "prefil": prefil})
            except:
                email = request.POST.get('email')
            try:
                phone = Student.objects.get(phone=phone)
                errors.append("Phone number Already Taken")
                return render(request, "accounts/signup.html", {"errors": errors, "prefil": prefil})
            except:
                phone = request.POST.get('phone')
            try:
                name = Institute.objects.get(name=name)
                errors.append("Institute Already Registered")
                return render(request, "accounts/signup.html", {"errors": errors, "prefil": prefil})
            except:
                name = request.POST.get('name')
            user = User(username=username, first_name=firstname,
                        last_name=lastname, password=password, email=email)
            user.save()
            Student(user=user, address=address, phone=phone).save()
            auth.login(request, user)
            request.session["user"] = username
            request.session["type"] = request.POST['type']
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
