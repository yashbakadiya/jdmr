from django.shortcuts import render, redirect, HttpResponse
from .models import BatchTiming, BatchTimingTutor, Notice
from courses.models import Courses
from accounts.models import Institute, Teacher
from django.contrib.auth.models import User
import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from .serializers import BatchTimingSerializer, BatchTimingTutorSerializer, NoticeSerializer
from django.core import serializers


@api_view(["POST", "GET", "PATCH", "DELETE"])
def BatchTimingAPI(request):
    if request.method == "GET":
        bt = BatchTiming.objects.all()
        bt = serializers.serialize('json', bt)
        return HttpResponse(bt, content_type="text/json-comment-filtered")
    data = request.data

    if request.session["type"] == "Institute":
        if request.method == "POST":
            batchName = data['batchName']
            days = data['days']
            startTime = data['startTime']
            endTime = data['endTime']
            original24time = data['original24time']
            user = User.objects.get(username=request.user)
            institute = Institute.objects.get(user=user)
            data['institute'] = institute.pk
            courseID = data['courseID']
            course = Courses.objects.filter(courseID=courseID).first()
            data['course'] = course.pk
            forclass = data['forclass']
            bts = BatchTimingSerializer(data=data)
            if bts.is_valid():
                bts.save()
                data['success'] = "Batch Timing Added Successfully"
            else:
                data['error'] = bts.errors
                return Response(data)
        elif request.method == "PATCH":
            user = User.objects.get(username=request.user)
            institute = Institute.objects.get(user=user)
            data['institute'] = institute.pk
            forclass = data['forclass']
            pk = data['pk']
            bts = BatchTiming.objects.get(pk=pk)
            bts = BatchTimingSerializer(bts, data=data, partial=True)
            if bts.is_valid():
                bts.save()
                data['success'] = "Batch Timing Updated Successfully!"
            else:
                data['error'] = bts.errors
                return Response(data)
        elif request.method == "DELETE":
            pk = data["pk"]
            bts = BatchTiming.objects.get(pk=pk)
            bts.delete()
            data['success'] = "Batch Timing Deleted Successfully"
        else:
            data['error'] = "Method is not POST"
            return Response(data)
    else:
        data['error'] = "Not an Institute Login"
        return Response(data)
    return Response(data)


@api_view(["POST", "GET", "PATCH", "DELETE"])
def NoticeAPI(request):
    if request.method == "GET":
        bt = Notice.objects.all()
        bt = serializers.serialize('json', bt)
        return HttpResponse(bt, content_type="text/json-comment-filtered")
    data = request.data

    if request.session["type"] == "Institute":
        if request.method == "POST":
            batch = data['batchName']
            batch = BatchTiming.objects.get(batchName=batch)
            data['batch'] = batch.pk
            ns = NoticeSerializer(data=data)
            if ns.is_valid():
                ns.save()
                data['success'] = "Notice Added Successfully"
            else:
                data['error'] = ns.errors
                return Response(data)
        elif request.method == "PATCH":
            pk = data['pk']
            ns = Notice.objects.get(pk=pk)
            ns = NoticeSerializer(ns, data=data, partial=True)
            if ns.is_valid():
                ns.save()
                data['success'] = "Notice Updated Successfully!"
            else:
                data['error'] = ns.errors
                return Response(data)
        elif request.method == "DELETE":
            pk = data["pk"]
            ns = Notice.objects.get(pk=pk)
            ns.delete()
            data['success'] = "Notice Deleted Successfully"
        else:
            data['error'] = "Method is not POST"
            return Response(data)
    else:
        data['error'] = "Not an Institute Login"
        return Response(data)
    return Response(data)


# TO DO
''' IT IS INCOMPLETE 
BatchTimingTutor View ave involvement of Tutor app 
After creating apis for tutor app COMPLETE This
'''


@api_view(["POST", "GET", "PATCH", "DELETE"])
def BatchTimingTutorAPI(request):
    if request.method == "GET":
        btt = BatchTimingTutor.objects.all()
        btt = serializers.serialize('json', btt)
        return HttpResponse(btt, content_type="text/json-comment-filtered")
    data = request.data

    if request.session["type"] == "Teacher":
        if request.method == "POST":
            batchName = data['batchName']
            days = data['days']
            startTime = data['startTime']
            endTime = data['endTime']
            original24time = data['original24time']
            user = User.objects.get(username=request.user)
            teacher = Teacher.objects.get(user=user)
            data['tutor'] = teacher.pk
            btts = BatchTimingTutorSerializer(data=data)
            if btts.is_valid():
                btts.save()
                data['success'] = "Batch Timing Tutor Added Successfully"
            else:
                data['error'] = btts.errors
                return Response(data)
        elif request.method == "PATCH":
            user = User.objects.get(username=request.user)
            institute = Institute.objects.get(user=user)
            data['institute'] = institute.pk
            forclass = data['forclass']
            pk = data['pk']
            bts = BatchTiming.objects.get(pk=pk)
            bts = BatchTimingSerializer(bts, data=data, partial=True)
            if bts.is_valid():
                bts.save()
                data['success'] = "Batch Timing Updated Successfully!"
            else:
                data['error'] = bts.errors
                return Response(data)
        elif request.method == "DELETE":
            pk = data["pk"]
            bts = BatchTiming.objects.get(pk=pk)
            bts.delete()
            data['success'] = "Batch Timing Deleted Successfully"
        else:
            data['error'] = "Method is not POST"
            return Response(data)
    else:
        data['error'] = "Not an Institute Login"
        return Response(data)
    return Response(data)
