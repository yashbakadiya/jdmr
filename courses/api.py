from django.shortcuts import render, redirect, HttpResponse
from .models import Courses, TeachingType
from accounts.models import Institute
from django.contrib.auth.models import User
import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from .serializers import TeachingTypeSerializer, CoursesSerializer
from django.core import serializers


@api_view(["POST", "GET", "PATCH", "DELETE"])
def CourseAPI(request):
    if request.method == "GET":
        courses = Courses.objects.all()
        courses = serializers.serialize('json', courses)
        return HttpResponse(courses, content_type="text/json-comment-filtered")
    data = request.data
    data['forclass'] = ', '.join(data['forclass'])
    forclass = data['forclass']
    user = User.objects.get(username=request.user)
    institute = Institute.objects.get(user=user)
    data['intitute'] = institute.pk
    coursename = data['courseName']
    count = (Courses.objects.all().count())+1
    course_ID = coursename[:3] + str("%03d" % count)
    data['courseID'] = course_ID

    if request.session["type"] == "Institute":
        if request.method == "POST":
            course = CoursesSerializer(data=data)
            if course.is_valid():
                course.save()
                data['success'] = "Course Added Successfully!"
            else:
                data['error'] = course.errors
                return Response(data)
        elif request.method == "PATCH":
            pk = data['pk']
            c = Courses.objects.get(pk=pk)
            course = CoursesSerializer(c, data=data, partial=True)
            if course.is_valid():
                course.save()
                data['success'] = "Course Updated Successfully!"
            else:
                data['error'] = course.errors
                return Response(data)
        elif request.method == "DELETE":
            pk = data["pk"]
            c = Courses.objects.get(pk=pk)
            c.delete()
            data['success'] = "Course Deleted Successfully"
        else:
            data['error'] = "Method is not POST"
            return Response(data)
    else:
        data['error'] = "Not an Institute Login"
        return Response(data)
    return Response(data)


@api_view(["POST", "GET"])
def TeachingTypeAPI(request):
    if request.method == "GET":
        teachingType = TeachingType.objects.all()
        teachingType = serializers.serialize('json', teachingType)
        return HttpResponse(teachingType, content_type="text/json-comment-filtered")
    data = request.data
    courseID = data['courseID']
    data['forclass'] = ', '.join(data['forclass'])
    forclass = data['forclass']
    teachtype = data['teachtype']
    duration = data['duration']
    timePeriod = data['timePeriod']
    user = User.objects.get(username=request.user)
    institute = Institute.objects.get(user=user)
    data['intitute'] = institute.pk
    course = Courses.objects.filter(courseID=courseID).first()
    data['course'] = course.pk
    data['courseID'] = data['course']
    if request.session["type"] == "Institute":
        if request.method == "POST":
            ttype = TeachingTypeSerializer(data=data)
            if ttype.is_valid():
                ttype.save()
                data['success'] = "Teaching Type Added Successfully!"
            else:
                data['error'] = ttype.errors
                return Response(data)
        elif request.method == "PATCH":
            pk = data['pk']
            c = TeachingType.objects.get(pk=pk)
            ttype = TeachingTypeSerializer(c, data=data, partial=True)
            if ttype.is_valid():
                ttype.save()
                data['success'] = "Teaching Type Updated Successfully!"
            else:
                data['error'] = ttype.errors
                return Response(data)
        elif request.method == "DELETE":
            pk = data["pk"]
            c = TeachingType.objects.get(pk=pk)
            c.delete()
            data['success'] = "Teaching Type Deleted Successfully"
        else:
            data['error'] = "Method is not POST"
            return Response(data)
    else:
        data['error'] = "Not an Institute Login"
        return Response(data)
    return Response(data)
