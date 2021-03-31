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

@api_view(['POST', 'GET'])
def buyInstituteNotes(request,id):
    if request.session['type'] == "Student":
        user = User.objects.get(username=request.user)
        student = Student.objects.get(user=user)
        note = NotesInstitute.objects.get(id=id)
        data = request.data
        data['student'] = student.id
        data['note'] = note.id
        data['status'] = 1
        if request.method == "GET":
            if int(note.price) == 0:
                buyData = BuyInstituteNotesSerializer(data=data)
                if buyData.is_valid():
                    buyData.save()
                    data['success'] = "Notes Bought Successfully!"
                else:
                    data['error'] = "something error!"
                    return redirect('notes-tutor-api')
            else:
                return Response(data)
                
        elif request.method == "POST":
            buyData = BuyInstituteNotesSerializer(data=data)
            if buyData.is_valid():
                buyData.save()
                data['success'] = "Notes Bought Successfully!"
            else:
                data['error'] = "something error!"
            return redirect('notes-tutor-api')
        return HttpResponse("method not found")
    return HttpResponse("You are Not Authenticated for this page")





@api_view(['POST', 'GET'])
def buyInstituteTutorial(request,id):
    if request.session['type'] == "Student":
        user = User.objects.get(username=request.user)
        student = Student.objects.get(user=user)
        tutorial = TutorialInstitute.objects.get(id=id)
        data = request.data
        data['student'] = student.id
        data['tutorial'] = tutorial.id
        data['status'] = 1
        if request.method == "GET":
            if int(note.price) == 0:
                buyData = BuyInstituteTutorialSerializer(data=data)
                if buyData.is_valid():
                    buyData.save()
                    data['success'] = "Notes Bought Successfully!"
                else:
                    data['error'] = "something error!"
                    return redirect('view-tutorial-tutor-api')
            else:
                return Response(data)

        
        elif request.method == "POST":
            buyData = BuyInstituteTutorialSerializer(data=data)
            if buyData.is_valid():
                buyData.save()
                data['success'] = "Notes Bought Successfully!"
            else:
                data['error'] = "something error!"
            return redirect('view-tutorial-tutor-api')
        return HttpResponse("method not found")
    return HttpResponse("You are Not Authenticated for this page")





@api_view(['POST', 'GET'])
def buyTutorExam(request,id):
    if request.session['type'] == "Student":
        user = User.objects.get(username=request.user)
        student = Student.objects.get(user=user)
        exam = TutorExam.objects.get(id=id)
        data = request.data
        data['student'] = student.id
        data['exam'] = exam.id
        data['status'] = 1
        if request.method == "GET":
            if int(note.price) == 0:
                buyData = BuyTutorExamSerializer(data=data)
                if buyData.is_valid():
                    buyData.save()
                    data['success'] = "Notes Bought Successfully!"
                else:
                    data['error'] = "something error!"
                    return redirect('viewexamstutor')
            else:
                return Response(data)
        
        elif request.method == "POST":
            buyData = BuyTutorExamSerializer(data=data)
            if buyData.is_valid():
                buyData.save()
                data['success'] = "Notes Bought Successfully!"
            else:
                data['error'] = "something error!"
            return redirect('viewexamstutor')
        return HttpResponse("method not found")
    return HttpResponse("You are Not Authenticated for this page")





@api_view(['POST', 'GET'])
def buyTutorNotes(request,id):
    if request.session['type'] == "Student":
        user = User.objects.get(username=request.user)
        student = Student.objects.get(user=user)
        note = NotesTutor.objects.get(id=id)
        data = request.data
        data['student'] = student.id
        data['note'] = note.id
        data['status'] = 1
        if request.method == "GET":
            if int(note.price) == 0:
                buyData = BuyTutorNotesSerializer(data=data)
                if buyData.is_valid():
                    buyData.save()
                    data['success'] = "Notes Bought Successfully!"
                else:
                    data['error'] = "something error!"
                    return redirect('notes-tutor-api')
            else:
                return Response(data)
      
        elif request.method == "POST":
            buyData = BuyTutorNotesSerializer(data=data)
            if buyData.is_valid():
                buyData.save()
                data['success'] = "Notes Bought Successfully!"
            else:
                data['error'] = "something error!"
            return redirect('notes-tutor-api')
        return HttpResponse("method not found")
    return HttpResponse("You are Not Authenticated for this page")


@api_view(['POST', 'GET'])
def buyTutorTutorial(request,id):
    if request.session['type'] == "Student":
        user = User.objects.get(username=request.user)
        student = Student.objects.get(user=user)
        tutorial = TutorialTutors.objects.get(id=id)
        data = request.data
        data['student'] = student.id
        data['tutorial'] = tutorial.id
        data['status'] = 1
        if request.method == "GET":
            if int(note.price) == 0:
                buyData = BuyTutorTutorialSerializer(data=data)
                if buyData.is_valid():
                    buyData.save()
                    data['success'] = "Notes Bought Successfully!"
                else:
                    data['error'] = "something error!"
                    return redirect('view-tutorial-tutor-api')
            else:
                return Response(data)
      
        elif request.method == "POST":
            buyData = BuyTutorTutorialSerializer(data=data)
            if buyData.is_valid():
                buyData.save()
                data['success'] = "Notes Bought Successfully!"
            else:
                data['error'] = "something error!"
            return redirect('view-tutorial-tutor-api')
        return HttpResponse("method not found")
    return HttpResponse("You are Not Authenticated for this page")

