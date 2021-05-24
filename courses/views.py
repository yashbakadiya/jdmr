from django.shortcuts import render, redirect, HttpResponse
from .models import Courses, TeachingType
from accounts.models import Institute, Teacher, Student
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.models import User
import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from .serializers import TeachingTypeSerializer, CoursesSerializer
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, JsonResponse

# Create your views here.


@login_required(login_url='Login')
def courses(request):
    with open('cc.txt') as f:
        data = f.read()
        data = json.loads(data)
        f.close()

    if request.session['type'] == "Institute":
        user = User.objects.get(username=request.session['user'])
        inst = Institute.objects.get(user=user)
        courses = Courses.objects.filter(intitute=inst, archieved=False)

        params = {'course': courses, 'data': data}

        if request.method == "POST":
            courseName = request.POST.get('selectcourse')
            forclass = request.POST.get('forclass')

            user = User.objects.get(username=request.session['user'])
            institute = Institute.objects.get(user=user)
            count = (Courses.objects.all().count())+1
            course_ID = courseName[:3] + str("%03d" % count)

            if not Courses.objects.filter(intitute=institute, forclass=forclass, courseName=courseName).exists():
                Courses(intitute=institute,
                        forclass=forclass,
                        courseName=courseName,
                        courseID=course_ID).save()

                if forclass == 'Other':
                    if courseName.lower() not in [x.lower() for x in data['Other']]:
                        data['Other'].append(courseName.capitalize())
                        data['Other'] = sorted(data['Other'])

                        with open('cc.txt', mode='w', encoding='utf-8') as fw:
                            fw.write(data)
                            fw.close()
                messages.success(request, 'Course Added successfully.')
                return redirect('courses')
            else:
                messages.warning(request, 'Course Already Exists!!! ',
                                 extra_tags='alert alert-warning alert-dismissible show')

        return render(request, 'courses-2/courses.html', params)
    return HttpResponse("You Are Not Authenticated for this Page")


@login_required(login_url="Login")
def editCourse(request, id):
    with open('cc.txt') as f:
        data = f.read()
        data = json.loads(data)
        f.close()

    if request.session['type'] == "Institute":
        try:
            cour = Courses.objects.get(id=id)
        except:
            return HttpResponse("Unable to edit")

        user = User.objects.get(username=request.session['user'])
        inst = Institute.objects.get(user=user)

        params = {'course': cour, 'data': data}

        if request.method == 'POST':
            courseName = request.POST.get('selectcourse')
            forclass = request.POST.get('forclass')

            user = User.objects.get(username=request.session['user'])
            institute = Institute.objects.get(user=user)

            if not Courses.objects.filter(intitute=institute, forclass=forclass, courseName=courseName).exists():
                cour.forclass = forclass
                cour.courseName = courseName
                cour.save()

                if forclass == 'Other':
                    if courseName.lower() not in [x.lower() for x in data['Other']]:
                        data['Other'].append(courseName.capitalize())
                        data['Other'] = sorted(data['Other'])

                        with open('cc.txt', mode='w', encoding='utf-8') as fw:
                            fw.write(data)
                            fw.close()
                messages.success(request, 'Course Added successfully.')
                return redirect('courses')
            else:
                messages.warning(request, 'Course Already Exists!!! ',
                                 extra_tags='alert alert-warning alert-dismissible show')

        return render(request, 'courses-2/editCourse2.html', params)

    return HttpResponse("You Are Not Authenticated for this Page")


@login_required(login_url='Login')
def courseArchive(request, id):
    if request.session['type'] == "Institute":
        user = User.objects.get(username=request.session['user'])
        inst = Institute.objects.get(user=user)

        course = Courses.objects.get(id=id)
        course.archieved = True
        course.save()
        messages.warning(request, "Course Added to Archive Succssfully")
        return redirect("courses")
    return HttpResponse("You Are Not Authenticated for this Page")


@login_required(login_url='Login')
def courseArchiveList(request):
    if request.session['type'] == "Institute":
        user = User.objects.get(username=request.session['user'])
        inst = Institute.objects.get(user=user)

        courses = Courses.objects.filter(intitute=inst, archieved=True)
        params = {'course': courses}
        return render(request, 'courses-2/archive-courses.html', params)
    return HttpResponse("You Are Not Authenticated for this Page")


@login_required(login_url='Login')
def courseUnArchive(request, id):
    if request.session['type'] == "Institute":
        user = User.objects.get(username=request.session['user'])
        inst = Institute.objects.get(user=user)
        courses = Courses.objects.filter(intitute=inst, archieved=True)

        course_archive = Courses.objects.get(id=id)
        course_archive.archieved = False
        course_archive.save()
        messages.success(request, "Course Removed from Archive Successfully")
        return redirect("courses")
        return render(request, 'courses-2/archive-teaching.html', params)
    return HttpResponse("You Are Not Authenticated for this Page")


@login_required(login_url="Login")
def deleteCourse(request, id):
    if request.session['type'] == "Institute":
        user = User.objects.get(username=request.session['user'])
        inst = Institute.objects.get(user=user)
        course = Courses.objects.get(id=id, intitute=inst)
        course.delete()

        messages.success(request, "Course Deleted Succssfully")
        return redirect("courses")
    return HttpResponse("You Are Not Authenticated for this Page")


@login_required(login_url='Login')
def teachingType2(request):
    if request.session['type'] == "Institute":
        user = User.objects.get(username=request.session['user'])
        inst = Institute.objects.get(user=user)
        forclass = Courses.objects.filter(
            intitute=inst, archieved=False).values_list('forclass').distinct()

        teach = TeachingType.objects.filter(
            course__intitute=inst, archieved=False)
        params = {'teach': teach,
                  'classes': forclass}

        if request.method == "POST":
            courseID = request.POST.get('courseName')

            forclass = request.POST.get('forclass')
            teachType1 = request.POST.getlist('teaching')
            teachType = ','.join(teachType1)

            duration1 = request.POST.getlist('duration')
            duration = ','.join(duration1)
            timePeriod1 = request.POST.getlist('time')
            timePeriod = ','.join(timePeriod1)
            if not TeachingType.objects.filter(courseID=courseID, forclass=forclass):
                course = Courses.objects.get(id=courseID)
                teachingtype = TeachingType(course=course,
                                            courseID=int(courseID),
                                            forclass=forclass,
                                            teachType=teachType,
                                            duration=duration,
                                            timePeriod=timePeriod).save()
                messages.success(request, "Teaching Type Added Successfully")
            else:
                messages.warning(request, "Teaching Type Already Exists")
            return redirect('teaching-type-2')

        return render(request, 'courses-2/teaching-type.html', params)
    return HttpResponse("You Are Not Authenticated for this Page")


@login_required(login_url="Login")
def editTeachingType(request, id):
    if request.session['type'] == "Institute":
        user = User.objects.get(username=request.session['user'])
        inst = Institute.objects.get(user=user)
        teach = TeachingType.objects.get(id=id)
        classes = Courses.objects.filter(
            intitute=inst, archieved=False).values_list('forclass').distinct()
        courseID = int(teach.courseID)
        params = {'teach': teach, 'classes': classes}
        if request.method == "POST":
            courseID = request.POST.get('courseName')
            forclass1 = request.POST.getlist('forclass', '')
            forclass = ','.join(forclass1)
            teachType1 = request.POST.getlist('teaching')
            teachType = ','.join(teachType1)

            duration1 = request.POST.getlist('duration')
            duration = ','.join(duration1)
            timePeriod1 = request.POST.getlist('time')
            timePeriod = ','.join(timePeriod1)

            course = Courses.objects.get(id=courseID)
            teach.course = course
            teach.courseID = int(courseID)
            teach.forclass = forclass
            teach.teachType = teachType
            teach.duration = duration
            teach.timePeriod = timePeriod
            teach.save()
            messages.success(request, 'Teaching Type Edited Successfully')
            return redirect('teaching-type-2')
        return render(request, 'courses-2/editTeachingType.html', params)
    return HttpResponse("You Are Not Authenticated for this Page")


def deleteteaching(request, id):
    if request.session['type'] == "Institute":
        user = User.objects.get(username=request.session['user'])
        inst = Institute.objects.get(user=user)
        course = TeachingType.objects.get(id=id)
        course.delete()
        messages.warning(request, "Teaching Type Deleted Succssfully")
        return redirect("teaching-type-2")
    return HttpResponse("You Are Not Authenticated for this Page")


@login_required(login_url='Login')
def teachingArchive(request, id):
    if request.session['type'] == "Institute":
        user = User.objects.get(username=request.session['user'])
        inst = Institute.objects.get(user=user)

        teaching = TeachingType.objects.get(id=id)
        teaching.archieved = True
        teaching.save()
        messages.warning(request, "Teaching Type Added to Archive Succssfully")
        return redirect("teaching-type-2")
    return HttpResponse("You Are Not Authenticated for this Page")


@login_required(login_url='Login')
def teachArchiveList(request):
    if request.session['type'] == "Institute":
        user = User.objects.get(username=request.session['user'])
        inst = Institute.objects.get(user=user)
        teach = TeachingType.objects.filter(
            course__intitute=inst, archieved=True)
        params = {'teach': teach}
        return render(request, 'courses-2/archive-teaching.html', params)
    return HttpResponse("You Are Not Authenticated for this Page")


@login_required(login_url='Login')
def teachUnArchive(request, id):
    if request.session['type'] == "Institute":
        user = User.objects.get(username=request.session['user'])
        inst = Institute.objects.get(user=user)
        teach = TeachingType.objects.filter(
            course__intitute=inst, archieved=True)

        teach_type = TeachingType.objects.get(id=id)
        teach_type.archieved = False
        teach_type.save()
        messages.success(request, "Teaching Removed from Archive Successfully")
        return redirect("teaching-type-2")

    return HttpResponse("You Are Not Authenticated for this Page")


def FindCoursesclass(request):
    courses = {}
    forclass = request.GET.get('forclass')

    if forclass:
        course_obj = Courses.objects.filter(forclass=forclass)
        courses = []
        for i in course_obj:
            courses.append((i.id, i.courseName))
    return JsonResponse({'courses': courses})
