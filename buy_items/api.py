# Django
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.core import serializers

# Rest framework
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets

# python
import json

# local
from .serializers import (
    BuyInstituteNotesSerializer,
    BuyInstituteTutorialSerializer,
    BuyTutorExamSerializer,
    BuyTutorNotesSerializer,
    BuyTutorTutorialSerializer
)
from notes.models import NotesInstitute, NotesTutor
from tutorials.models import TutorialInstitute, TutorialTutors
from exams.models import TutorExam
from accounts.models import Institute, Teacher, Student


@api_view(['POST', 'GET'])
def buyInstituteNotesAPI(request,id):
    if request.session['type'] == "Student":
        user = User.objects.get(username=request.user)
        student = Student.objects.get(user=user)
        note = NotesInstitute.objects.get(id=id)
        
        if request.method == "GET":
            data = {}
            data['student'] = student.id
            data['note'] = note.id
            data['status'] = 1
            if int(note.price) == 0:
                buyData = BuyInstituteNotesSerializer(data=data)
                if buyData.is_valid():
                    buyData.save()
                    data['success'] = "Notes Bought Successfully!"
                else:
                    data['error'] = "something error!"
                    return redirect('notesstudents')
            else:
                return Response(data)
                
        elif request.method == "POST":
            data = request.data
            data['student'] = student.id
            data['note'] = note.id
            data['status'] = 1
            buyData = BuyInstituteNotesSerializer(data=data)
            if buyData.is_valid():
                buyData.save()
                data['success'] = "Notes Bought Successfully!"
            else:
                data['error'] = "something error!"
            return redirect('notesstudents')
        return HttpResponse("method not found")
    return HttpResponse("You are Not Authenticated for this page")





@api_view(['POST', 'GET'])
def buyInstituteTutorialAPI(request,id):
    if request.session['type'] == "Student":
        user = User.objects.get(username=request.user)
        student = Student.objects.get(user=user)
        tutorial = TutorialInstitute.objects.get(id=id)

        if request.method == "GET":
            data = {}
            data['student'] = student.id
            data['tutorial'] = tutorial.id
            data['status'] = 1
            if int(tutorial.Fees) == 0:
                buyData = BuyInstituteTutorialSerializer(data=data)
                if buyData.is_valid():
                    buyData.save()
                    data['success'] = "Notes Bought Successfully!"
                else:
                    data['error'] = "something error!"
                    return redirect('searchcourses')
            else:
                return Response(data)

        elif request.method == "POST":
            data = request.data
            data['student'] = student.id
            data['tutorial'] = tutorial.id
            data['status'] = 1
            buyData = BuyInstituteTutorialSerializer(data=data)
            if buyData.is_valid():
                buyData.save()
                data['success'] = "Notes Bought Successfully!"
            else:
                data['error'] = "something error!"
            return redirect('searchcourses')
        return HttpResponse("method not found")
    return HttpResponse("You are Not Authenticated for this page")





@api_view(['POST', 'GET'])
def buyTutorExamAPI(request,id):
    if request.session['type'] == "Student":
        user = User.objects.get(username=request.user)
        student = Student.objects.get(user=user)
        exam = TutorExam.objects.get(id=id)
        
        if request.method == "GET":
            data = {}
            data['student'] = student.id
            data['exam'] = exam.id
            data['status'] = 1
            if int(exam.price) == 0:
                buyData = BuyTutorExamSerializer(data=data)
                if buyData.is_valid():
                    buyData.save()
                    data['success'] = "Notes Bought Successfully!"
                else:
                    data['error'] = "something error!"
                    return redirect('studentexams')
            else:
                return Response(data)
        
        elif request.method == "POST":
            data = request.data
            data['student'] = student.id
            data['exam'] = exam.id
            data['status'] = 1
            buyData = BuyTutorExamSerializer(data=data)
            if buyData.is_valid():
                buyData.save()
                data['success'] = "Notes Bought Successfully!"
            else:
                data['error'] = "something error!"
            return redirect('studentexams')
        return HttpResponse("method not found")
    return HttpResponse("You are Not Authenticated for this page")




@api_view(['POST', 'GET'])
def buyTutorNotesAPI(request,id):
    if request.session['type'] == "Student":
        user = User.objects.get(username=request.user)
        student = Student.objects.get(user=user)
        note = NotesTutor.objects.get(id=id)
        
        if request.method == "GET":
            data = {}
            data['student'] = student.id
            data['note'] = note.id
            data['status'] = 1
            if int(note.price) == 0:
                buyData = BuyTutorNotesSerializer(data=data)
                if buyData.is_valid():
                    buyData.save()
                    data['success'] = "Notes Bought Successfully!"
                else:
                    data['error'] = "something error!"
                    return redirect('notesstudents')
            else:
                return Response(data)
      
        elif request.method == "POST":
            data = request.data
            data['student'] = student.id
            data['note'] = note.id
            data['status'] = 1
            buyData = BuyTutorNotesSerializer(data=data)
            if buyData.is_valid():
                buyData.save()
                data['success'] = "Notes Bought Successfully!"
            else:
                data['error'] = "something error!"
            return redirect('notesstudents')
        return HttpResponse("method not found")
    return HttpResponse("You are Not Authenticated for this page")


@api_view(['POST', 'GET'])
def buyTutorTutorialAPI(request,id):
    if request.session['type'] == "Student":
        user = User.objects.get(username=request.user)
        student = Student.objects.get(user=user)
        tutorial = TutorialTutors.objects.get(id=id)
        
        if request.method == "GET":
            data = {}
            data['student'] = student.id
            data['tutorial'] = tutorial.id
            data['status'] = 1
            if int(tutorial.Fees) == 0:
                buyData = BuyTutorTutorialSerializer(data=data)
                if buyData.is_valid():
                    buyData.save()
                    data['success'] = "Notes Bought Successfully!"
                else:
                    data['error'] = "something error!"
                    return redirect('searchcourses')
            else:
                return Response(data)
      
        elif request.method == "POST":
            data = request.data
            data['student'] = student.id
            data['tutorial'] = tutorial.id
            data['status'] = 1
            buyData = BuyTutorTutorialSerializer(data=data)
            if buyData.is_valid():
                buyData.save()
                data['success'] = "Notes Bought Successfully!"
            else:
                data['error'] = "something error!"
            return redirect('searchcourses')
        return HttpResponse("method not found")
    return HttpResponse("You are Not Authenticated for this page")

