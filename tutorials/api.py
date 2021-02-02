from django.shortcuts import render, redirect, HttpResponse
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
from teacher.models import enrollTutors
from .models import *


@api_view(["GET", "POST"])
def AddTutorialInstituteAPI(request):
    data = request.data
    if data["type"] == "Institute":
        username = data['username']
        username = User.objects.get(username=username)
        inst = Institute.objects.get(user=username)
        courses = Courses.objects.filter(intitute=inst, archieved=False)

        if request.method == "POST":
            title = data['title']
            description = data['description']
            fees = data['fees']
            duration = data["duration"]
            course = data["course"]
            feeDisc = data["feeDisc"]
            discValidity = data["discValidity"]
            discValidity = datetime.strptime(discValidity, '%Y-%m-%d')
            data1 = TutorialInstitute(
                Title=title,
                Course=Courses.objects.get(intitute=inst, courseID=course),
                Fees=fees,
                Duration=duration,
                Description=description,
                Validity=discValidity,
                Discount=feeDisc,
            )
            data1.save()
            data["success"] = "Institute Tutorial Saved Successfully"
            return Response(data)
    data['error'] = "Not Authenticated"
    return Response(data)


@api_view(["GET", "POST"])
def ViewTutorialsAPI(request):
    data = request.data
    if data["type"] == "Institute":
        username = data['username']
        username = User.objects.get(username=username)
        inst = Institute.objects.get(user=username)
        courses = Courses.objects.filter(intitute=inst, archieved=False)
        data['courses'] = courses
        tutorials = []
        try:
            for i in courses:
                if TutorialInstitute.objects.filter(Course=i).exists():
                    tutorials.extend(TutorialInstitute.objects.filter(
                        Q(Course=i) & Q(Archived=False)))
        except:
            tutorials = []
        data["tutorials"] = tutorials
        if request.method == "POST":
            ids = data['archive-list']
            if len(ids) < 1:
                data["error"] = "No Id found in archive-list"
                return Response(data)
            for i in ids:
                if TutorialInstitute.objects.filter(id=i).exists():
                    tutorial = TutorialInstitute.objects.get(id=int(i))
                    tutorial.Archived = True
                    tutorial.save()
            data["success"] = "Tutorial Archived"
            return Response(data)
        return Response(data)
    data['error'] = "Not Authenticated"
    return Response(data)


@api_view(["GET", "POST"])
def ArchiveTutorialsAPI(request):
    data = request.data
    if data["type"] == "Institute":
        username = data['username']
        username = User.objects.get(username=username)
        inst = Institute.objects.get(user=username)
        courses = Courses.objects.filter(intitute=inst, archieved=False)
        data['courses'] = courses
        tutorials = []
        try:
            for i in courses:
                if TutorialInstitute.objects.filter(Course=i).exists():
                    tutorials.extend(TutorialInstitute.objects.filter(
                        Q(Course=i) & Q(Archived=False)))
        except:
            tutorials = []
        data["tutorials"] = tutorials
        if request.method == "POST":
            ids = data['archive-list']
            if len(ids) < 1:
                data["error"] = "No Id found in archive-list"
                return Response(data)
            for i in ids:
                if TutorialInstitute.objects.filter(id=i).exists():
                    tutorial = TutorialInstitute.objects.get(id=int(i))
                    tutorial.Archived = True
                    tutorial.save()
            data["success"] = "Tutorial Archived"
            return Response(data)
        return Response(data)
    data['error'] = "Not Authenticated"
    return Response(data)


@api_view(["GET", "POST"])
def AddTutorialsInstituteVideosAPI(request):
    data = request.data
    tutorial = TutorialInstitute.objects.get(id=data["course-id"])
    errors = []
    if request.method == "POST":
        video = data["video"]
        title = data["title"]
        description = data["description"]
        try:
            for item in range(len(title)):
                data = TutorialInstitutePlaylist(
                    tutorial=tutorial,
                    Title=title[item],
                    Description=description[item],
                    Video=video[item])
                data.save()
        except:
            errors.append("File Field Must Not be Empty")
            data["errors"] = errors
            return Response(data)
        data["success"] = "Data Saved"
        return Response(data)
    return Response(data)


@api_view(["GET", "DELETE"])
def DeleteTutorialsInstituteAPI(request):
    data = request.data
    if data['type'] == "Institute":
        if request.method == "DELETE":
            data1 = TutorialInstitute.objects.get(id=data["course-id"])
            data1.delete()
            data["success"] = "Tutorial Deleted Successfully"
            return Response(data)
        data["error"] = "Not a valid request"
        return Response(data)
    data['error'] = "Not Authenticated"
    return Response(data)


@api_view(["GET", "PUT"])
def EditTutorialsInstituteAPI(request):
    data = request.data
    if data['type'] == "Institute":
        username = data['username']
        username = User.objects.get(username=username)
        inst = Institute.objects.get(user=username)
        courses = Courses.objects.filter(intitute=inst)
        tutorial = TutorialInstitute.objects.get(id=data["course-id"])
        data["tutorial"] = tutorial
        data["courses"] = courses
        if request.method == "PUT":
            title = data['title']
            description = data['description']
            fees = data['fees']
            duration = data["duration"]
            course = data["course"]
            feeDisc = data["feeDisc"]
            discValidity = data["discValidity"]
            if title:
                tutorial.Title = title
            if description:
                tutorial.Description = description
            if fees:
                tutorial.Fees = fees
            if duration:
                tutorial.Duration = duration
            if course:
                tutorial.Course = Courses.objects.get(
                    intitute=inst, courseName=course)
            if feeDisc:
                tutorial.Discount = feeDisc
            if discValidity:
                discValidity = datetime.strptime(discValidity, '%Y-%m-%d')
                tutorial.Validity = discValidity
            tutorial.save()
            data["success"] = "Tutorial Updated Successfully"
            return Response(data)
        data["error"] = "Not a valid Request for updating"
        return Response(data)
    data['error'] = "Not Authenticated"
    return Response(data)


@api_view(["GET", "POST"])
def WatchTutorialsInstituteAPI(request):
    data = request.data
    if data['type'] == "Institute":
        username = data['username']
        username = User.objects.get(username=username)
        inst = Institute.objects.get(user=username)
        courses = Courses.objects.filter(intitute=inst)
        tutorial = TutorialInstitute.objects.get(id=data["course-id"])
        data["tutorial"] = tutorial
        data["courses"] = courses
        course_id = data["course-id"]
        if request.session.has_key(f"Watching{course_id}"):
            start = request.session[f"Watching{course_id}"]
        else:
            if TutorialInstitutePlaylist.objects.filter(tutorial=tutorial).exists():
                start = TutorialInstitutePlaylist.objects.filter(
                    tutorial=tutorial).first().Video.url
                request.session[f"Watching{course_id}"] = start
        total_length = 0
        if TutorialInstitutePlaylist.objects.filter(tutorial=tutorial).exists():
            for item in TutorialInstitutePlaylist.objects.filter(tutorial=tutorial):
                total_length += item.Clip_Duration()

        total_length = f"{total_length} min"
        data.update({
            'tutorial': tutorial,
            'start': start,
            'total_length': total_length
        })
        return Response(data)
    data['error'] = "Not Authenticated"
    return Response(data)


@api_view(["GET", "DELETE"])
def DeleteTutorialsInstituteVideosAPI(request):
    data = request.data
    if data['type'] == "Institute":
        if request.method == "DELETE":
            playlist_id = data["playlist-id"]
            data1 = TutorialInstitutePlaylist.objects.get(id=playlist_id)
            data1.delete()
            data["success"] = "Tutorial Videos Deleted Successfully"
            return Response(data)
        data["error"] = "Not a valid request"
        return Response(data)
    data['error'] = "Not Authenticated"
    return Response(data)


@api_view(["GET", "PUT"])
def EditTutorialsInstituteVideoAPI(request):
    data = request.data
    if data['type'] == "Institute":
        username = data['username']
        username = User.objects.get(username=username)
        inst = Institute.objects.get(user=username)
        courses = Courses.objects.filter(intitute=inst)
        tutorial = TutorialInstitutePlaylist.objects.get(
            id=data["playlist-id"])
        data["tutorial"] = tutorial
        data["courses"] = courses
        if request.method == "PUT":
            video = data['video']
            title = data['title']
            description = data['description']
            if title:
                tutorial.Title = title
            if description:
                tutorial.Description = description
            if video:
                tutorial.Video = video
            tutorial.save()
            data["success"] = 'Tutorial Video Updated'
            return Response(data)
        data["error"] = "Not a valid request"
        return Response(data)
    data['error'] = "Not Authenticated"
    return Response(data)


@api_view(["GET", "POST"])
def AddTutorialsTutorAPI(request):
    data = request.data
    if data['type'] == "Teacher":
        user = User.objects.get(username=data["username"])
        tutor = Teacher.objects.get(user=user)
        tutorial = TutorialTutors.objects.get(
            id=data["course-id"])
        data["tutorial"] = tutorial
        errors = []
        if request.method == "POST":
            video = data["video"]
            title = data["title"]
            description = data["description"]
            try:
                for item in range(len(title)):
                    data1 = TutorialTutorsPlaylist(
                        tutorial=tutorial,
                        Title=title[item],
                        Description=description[item],
                        Video=video[item])
                    data1.save()
                return Response(data)
            except:
                errors.append("File Field Must Not be Empty")
                data["error"] = errors
                return Response(data)
        data["error"] = "Not a valid request"
        return Response(data)
    data['error'] = "Not Authenticated"
    return Response(data)


@api_view(["GET", "POST"])
def ViewTutorialsTutorAPI(request):
    data = request.data
    if data['type'] == "Teacher":
        user = User.objects.get(username=data["username"])
        tutor = Teacher.objects.get(user=user)
        tutorials = TutorialTutors.objects.filter(
            Q(Tutor=tutor) & Q(Archived=False))
        data["tutorials"] = tutorials
        if request.method == "POST":
            ids = data['archive-list']
            if len(ids) < 1:
                data["error"] = " No archive id found in archive-list"
                return Response(data)
            for i in ids:
                if TutorialTutors.objects.filter(id=i).exists():
                    tutorial = TutorialTutors.objects.get(id=int(i))
                    tutorial.Archived = True
                    tutorial.save()
                print('yes')
            data["success"] = "Tutors Archived"
            return Response(data)
        return Response(data)
    data['error'] = "Not Authenticated"
    return Response(data)


@api_view(["GET", "POST"])
def WatchTutorialsTutorAPI(request):
    data = request.data
    if data['type'] == "Teacher":
        user = User.objects.get(username=data["username"])
        tutor = Teacher.objects.get(user=user)
        course_id = data['course-id']
        tutorial = TutorialTutors.objects.get(id=course_id)
        data["tutorial"] = tutorial

        if request.session.has_key(f"WatchingTutor{course_id}"):
            start = request.session[f"WatchingTutor{course_id}"]
        else:
            if TutorialTutorsPlaylist.objects.filter(tutorial=tutorial).exists():
                start = TutorialTutorsPlaylist.objects.filter(
                    tutorial=tutorial).first().Video.url
                request.session[f"WatchingTutor{course_id}"] = start
        total_length = 0

        if TutorialTutorsPlaylist.objects.filter(tutorial=tutorial).exists():
            for item in TutorialTutorsPlaylist.objects.filter(tutorial=tutorial):
                total_length += item.Clip_Duration()

        total_length = f"{total_length}min"
        data.update({
            'tutorial': tutorial,
            'start': start,
            'total_length': total_length
        })
        return Response(data)
    data['error'] = "Not Authenticated"
    return Response(data)


@api_view(["GET", "DELETE"])
def DeleteTutorialsTutorAPI(request):
    data = request.data
    if data['type'] == "Teacher":
        course_id = data['course-id']
        if request.method == "DELETE":
            data1 = TutorialTutors.objects.get(id=course_id)
            data1.delete()
            data["success"] = "Tutorial Tutor Deleted Successfully"
            return Response(data)
        data["error"] = "Not a valid request"
        return Response(data)
    data['error'] = "Not Authenticated"
    return Response(data)


@api_view(["GET", "DELETE"])
def DeleteTutorialsTutorVideosAPI(request):
    data = request.data
    if data['type'] == "Teacher":
        playlist_id = data['playlist-id']
        if request.method == "DELETE":
            data1 = TutorialTutorsPlaylist.objects.get(id=playlist_id)
            data1.delete()
            data["success"] = "Tutorial Tutor Video Deleted Successfully"
            return Response(data)
        data["error"] = "Not a valid request"
        return Response(data)
    data['error'] = "Not Authenticated"
    return Response(data)


@api_view(["GET", "PUT"])
def EditTutorialsTutorVideosAPI(request):
    data = request.data
    if data['type'] == "Teacher":
        tutorial = TutorialTutorsPlaylist.objects.get(
            id=data["playlist-id"])
        data["tutorial"] = tutorial
        if request.method == "PUT":
            video = data['video']
            title = data['title']
            description = data['description']
            if title:
                tutorial.Title = title
            if description:
                tutorial.Description = description
            if video:
                tutorial.Video = video
            tutorial.save()
            data["success"] = 'Tutorial Video Updated'
            return Response(data)
        data["error"] = "Not a valid request"
        return Response(data)
    data['error'] = "Not Authenticated"
    return Response(data)


@api_view(["GET", "PUT"])
def EditTutorialsTutorAPI(request):
    data = request.data
    if data['type'] == "Teacher":
        course_id = data['course-id']
        user = User.objects.get(username=data["username"])
        tutorial = TutorialTutors.objects.get(id=course_id)
        tutorial = TutorialInstitute.objects.get(id=data["course-id"])
        data["tutorial"] = tutorial
        if request.method == "PUT":
            title = data['title']
            description = data['description']
            fees = data['fees']
            duration = data["duration"]
            feeDisc = data["feeDisc"]
            discValidity = data["discValidity"]
            if title:
                tutorial.Title = title
            if description:
                tutorial.Description = description
            if fees:
                tutorial.Fees = fees
            if duration:
                tutorial.Duration = duration
            if feeDisc:
                tutorial.Discount = feeDisc
            if discValidity:
                discValidity = datetime.strptime(discValidity, '%Y-%m-%d')
                tutorial.Validity = discValidity
            tutorial.save()
            data["success"] = "Tutorial Updated Successfully"
            return Response(data)
        data["error"] = "Not a valid Request for updating"
        return Response(data)
    data['error'] = "Not Authenticated"
    return Response(data)


@api_view(["GET", "POST"])
def ArchiveTutorialsTutorAPI(request):
    data = request.data
    if data["type"] == "Institute":
        username = data['username']
        user = User.objects.get(username=username)
        tutor = Teacher.objects.get(user=user)
        tutorials = TutorialTutors.objects.filter(
            Q(Tutor=tutor) & Q(Archived=True))
        data['tutorials'] = tutorials
        if request.method == "POST":
            ids = data['archive-list']
            if len(ids) < 1:
                data["error"] = "No Id found in archive-list"
                return Response(data)
            for i in ids:
                if TutorialTutors.objects.filter(id=i).exists():
                    tutorial = TutorialTutors.objects.get(id=int(i))
                    tutorial.Archived = True
                    tutorial.save()
            data["success"] = "Tutorial Tutor Archived"
            return Response(data)
        return Response(data)
    data['error'] = "Not Authenticated"
    return Response(data)


# Where is Add Courses Model


@api_view(["GET", "POST"])
def SearchCoursesAPI(request):
    data = request.data
    tutorials = TutorialTutors.objects.all()
    extra = TutorialInstitute.objects.all()
    courses = TutorialInstitute.objects.all()
    if request.method == 'POST':
        coursetype = data['type']
        duration = data['duration']
        fees = data['fees']
        if coursetype:
            extra = TutorialInstitute.objects.all().filter(
                Q(Course=AddCourses.objects.get(s_num=coursetype)))
            course = AddCourses.objects.get(s_num=coursetype).courseName
            tutorials = TutorialTutors.objects.all().filter(Title__icontains=course)

        if duration:
            if extra.exists():
                extra = extra.filter(Duration=duration)
            if tutorials.exists():
                tutorials = tutorials.filter(Duration=duration)
        if fees:
            fees = fees.split('-')
            if extra.exists():
                extra = extra.filter(
                    Q(Fees__gte=fees[0]) & Q(Fees__lte=fees[1]))
            if tutorials.exists():
                tutorials = tutorials.filter(
                    Q(Fees__gte=fees[0]) & Q(Fees__lte=fees[1]))

        if tutorials and extra:
            tutorials = tutorials.union(extra)
        elif extra:
            tutorials = extra
        else:
            tutorials = tutorials
        context = {
            'tutorials': tutorials,
            'courses': courses
        }
    data['error'] = "Not Authenticated"
    return Response(data)
