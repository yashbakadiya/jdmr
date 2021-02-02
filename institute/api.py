from django.shortcuts import render, redirect, HttpResponse
from .models import AddFeesC, SubmitFees, Instalment
from courses.models import Courses, TeachingType
from accounts.models import Institute, Teacher, Student
from django.contrib.auth.models import User
import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from .serializers import AddFeesSerializer, SubmitFeesSerializer, NewInstallmentSerializer
from django.core import serializers
from django.db.models import Q
from datetime import datetime, timedelta


# NEEDs Teacher App Model
@api_view(["POST", "GET", "PATCH", "DELETE"])
def InstituteTutorAPI(request):
    data = request.data
    type = data['type']
    pass
    if type == "Teacher":
        user = User.objects.get(username=data['username'])
        tutor = Teacher.objects.get(user=user)
        if enrollTutors.objects.filter(teacher=tutor).exists():
            INST = enrollTutors.objects.get(teacher=tutor)
            return render(request, "Institute/institute.html", {"INST": INST, "template": "dashboard/dashboardTutor.html"})
