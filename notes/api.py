from django.shortcuts import render, redirect, HttpResponse
from .models import NotesInstitute, NotesTutor
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
from .serializers import NotesInstituteSerializer
from teacher.models import enrollTutors


@api_view(["GET", "POST", "DELETE", "PATCH"])
def NotesInstituteAPI(request):
    data = request.data
    if data["type"] == "Institute":
        username = data['username']
        user = User.objects.get(username=username)
        inst = Institute.objects.get(user=user)
        courses = Courses.objects.filter(intitute=inst)
        data['courses'] = courses
        if request.method == "POST":
            note = data["note"]
            title = data["title"]
            description = data["description"]
            course = data["course"]
            if (note and title and description and course):
                data1 = NotesInstitute(
                    institute=inst,
                    notes=note,
                    title=title,
                    subject=course,
                    description=description,
                )
                try:
                    data1.save()
                    data['success'] = "Notes Saved"
                    return Response(data)
                except:
                    data['error'] = data1.errors
                    return Response(data)
        elif request.method == "GET":
            notes = NotesInstitute.objects.filter(institute=inst)
            data['notes'] = notes
            return Response(data)
        elif request.method == "DELETE":
            note = NotesInstitute.objects.get(id=data['note_id'])
            note.delete()
            data['success'] = "Notes Deleted"
            return Response(data)
        elif request.method == "PATCH":
            data1 = NotesInstitute.objects.get(id=data['note_id'])
            if "note" in data:
                note = data["note"]
            if "title" in data:
                title = data["title"]
            if "description" in data:
                description = data['discription']
            if "course" in data:
                course = data["course"]
            data1 = NotesInstituteSerializer(data1, data=data, partial=True)
            if data1.is_valid():
                data1.save()
                data['success'] = "Notes Updated!"
                return Response(data)
            else:
                data['error'] = data1.errors
                return Response(data)
    data['error'] = "Not Authenticated"
    return Response(data)


@api_view(["GET", "POST", "DELETE", "PATCH"])
def NotesTutorAPI(request):
    data = request.data
    if data["type"] == "Teacher":
        username = data['username']
        user = User.objects.get(username=username)
        tutor = Teacher.objects.get(user=user)
        if request.method == "GET":
            notes = NotesTutor.objects.filter(tutor=tutor)
            data['notes'] = notes
            return Response(data)
        elif request.method == "POST":
            note = data["note"]
            title = data["title"]
            description = data['discription']
            course = data["course"]
            if (note and title and description and course):
                data1 = NotesTutor(
                    tutor=tutor,
                    notes=note,
                    title=title,
                    subject=course,
                    description=description,
                )
                try:
                    data1.save()
                    data['success'] = "Tutor Notes Saved!"
                except:
                    data['errors'] = data1.errors
                return Response(data)
        elif request.method == "GET":
            notes = NotesTutor.objects.filter(tutor=tutor)
            data['notes'] = notes
            return Response(data)
        elif request.method == "DELETE":
            try:
                note = NotesTutor.objects.get(id=data['note_id'])
            except:
                data['error'] = "Unable to Process"
                return Response(data)
            if tutor == note.tutor:
                note.delete()
                data['success'] = "Tutor Note Deleted!"
                return Response(data)
            else:
                data["error"] = "You are not Authenticated for this Page"
                return Response(data)
        elif request.method == "PATCH":
            data1 = NotesTutor.objects.get(id=data['note_id'])
            if "note" in data:
                note = data["note"]
            if "title" in data:
                title = data["title"]
            if "description" in data:
                description = data['discription']
            if "course" in data:
                course = data["course"]
            data1 = NotesInstituteSerializer(data1, data=data, partial=True)
            if data1.is_valid():
                data1.save()
                data['success'] = "Tutor Notes Updated!"
                return Response(data)
            else:
                data['error'] = data1.errors
                return Response(data)
    data['error'] = "Not Authenticated"
    return Response(data)
