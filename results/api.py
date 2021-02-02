from django.http import response
from django.shortcuts import render, redirect, HttpResponse
from exams.models import Exam
from courses.models import Courses, TeachingType
from accounts.models import Institute, Teacher, Student
from django.contrib.auth.models import User
import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from django.core import serializers
from django.db.models import Q
from datetime import datetime, timedelta


# NEEDs Teacher App Model
# Needed Parameters 'type', 'username',
# GET Parameters
# None
@api_view(["GET"])
def CoachingResultStudentAPI(request):
    data = request.data
    if data['type'] == "Institute":
        user = User.objects.get(username=data['username'])
        inst = Institute.objects.get(user=user)
        if Exam.objects.filter(institute=inst).exists():
            exams = Exam.objects.filter(institute=inst)
            data['exams'] = exams
            return Response(data)
        return Response(data)
    data['error'] = "You Are Not Authenticated"
    return Response(data)
