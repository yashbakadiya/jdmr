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


@api_view(["POST", "GET"])
def loginApi(request):
    data = request.data
    username = data['username']
    password = data['password']
    print(request.data)
    if request.method == "POST":
        users = User.objects.values('username', 'password')
        for u in users:
            if u['username'] == username and u['password'] == password:
                user = User.objects.get(username=username, password=password)
                auth.login(request, user)
                request.session['type'] = data["type"]
                data["Success"] = "User has successfully logged In"
                return Response(data)
        data["error"] = "Invalid Credentials, Please try again"
    return Response(data)


@api_view(["POST", ])
def SignUpAPI(request):
    data = request.data
    username = data['username']
    firstname = data['firstname']
    lastname = data['lastname']
    password = data['password']
    confpassword = data['confpassword']
    email = data['email']
    phone = data['phone']
    address = data['address']
    user_type = data['type']
    userdata = {
        'email': email,
        'username': username,
        'password': password,
        'first_name': firstname,
        'last_name': lastname
    }
    if request.method == "POST":

        if password != confpassword:
            data["error"] = "Passwords do not match"
            return Response(data)
        if user_type == 'Institute':
            user_serializer = UserSerializer(
                data=data)
            if user_serializer.is_valid():
                try:
                    email = Institute.objects.get(user__email=email)
                    data["error"] = "Email Already Taken"
                    return Response(data)
                except:
                    email = data['email']
                try:
                    phone = Institute.objects.get(user__phone=phone)
                    data["error"] = "Mobile Number Already Taken"
                    return Response(data)
                except:
                    email = data['phone']
                try:
                    username = Institute.objects.get(user__username=username)
                    data["error"] = "Username Already Taken"
                    return Response(data)
                except:
                    username = data['username']
                user_serializer.save()
                User1 = User.objects.get(username=username)
                data['user'] = User1.pk
                institute_serializer = InstituteSerializer(data=data)
                if institute_serializer.is_valid():
                    institute_serializer.save()
                    data["Success"] = "Institute Added Successfully"
                else:
                    data["error"] = institute_serializer.errors
                    return Response(data)
            else:
                data["error"] = user_serializer.errors
                return Response(data)
        elif user_type == 'Teacher':
            user_serializer = UserSerializer(data=userdata)
            if user_serializer.is_valid():
                try:
                    email = Teacher.objects.get(user__email=email)
                    data["error"] = "Email Already Taken"
                    return Response(data)
                except:
                    email = data['email']
                try:
                    phone = Teacher.objects.get(user__phone=phone)
                    data["error"] = "Mobile Number Already Taken"
                    return Response(data)
                except:
                    email = data['phone']
                try:
                    username = Teacher.objects.get(user__username=username)
                    data["error"] = "Username Already Taken"
                    return Response(data)
                except:
                    username = data['username']
                user_serializer.save()
                User1 = User.objects.get(username=username)
                data['user'] = User1.pk
                teacher_serializer = TeacherSerializer(data=data)
                if teacher_serializer.is_valid():
                    teacher_serializer.save()
                    data["Success"] = "Teacher Added Successfully"
                else:
                    data["error"] = teacher_serializer.errors
                    return Response(data)
            else:
                data["error"] = user_serializer.errors
                return Response(data)
        elif user_type == 'Student':
            user_serializer = UserSerializer(data=userdata)
            if user_serializer.is_valid():
                try:
                    email = Student.objects.get(user__email=email)
                    data["error"] = "Email Already Taken"
                    return Response(data)
                except:
                    email = data['email']
                try:
                    phone = Student.objects.get(user__phone=phone)
                    data["error"] = "Mobile Number Already Taken"
                    return Response(data)
                except:
                    email = data['phone']
                try:
                    username = Student.objects.get(user__username=username)
                    data["error"] = "Username Already Taken"
                    return Response(data)
                except:
                    username = data['username']
                user_serializer.save()
                User1 = User.objects.get(username=username)
                data['user'] = User1.pk
                student_serializer = StudentSerializer(data=data)
                if student_serializer.is_valid():
                    student_serializer.save()
                    data["Success"] = "Student Added Successfully"
                else:
                    data["error"] = student_serializer.errors
                    return Response(data)
            else:
                data["error"] = user_serializer.errors
                return Response(data)
    else:
        data["error"] = "Method is not POST"
    return Response(data)
