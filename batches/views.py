from django.shortcuts import render, redirect, HttpResponse
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.models import Institute, Teacher, Student
from django.contrib.auth.models import User
from datetime import datetime, timedelta
import datetime as dt
from courses.models import Courses
from json import dumps, loads
import json
from django.http import JsonResponse
from teacher.models import enrollTutors
from django.db.models import Q
from batches.models import BatchTiming
# Create your views here.


def ampm(inpTime):
    print(inpTime)
    # converting 24 hour time to 12 hour time
    temp = inpTime.split(":")
    hour = int(temp[0])
    minute = temp[1]
    if(hour == 0):
        hour = 12
        ending = 'AM'
    elif(hour == 12):
        ending = 'PM'
    elif(hour > 12):
        hour = str(hour % 12).zfill(2)
        ending = 'PM'
    else:
        ending = 'AM'
    result = str(hour)+":"+str(minute)+":"+ending
    return result


@login_required(login_url='Login')
def batchTiming2(request):
    if request.session['type'] == 'Institute':
        if request.method == 'POST':
            user = User.objects.get(username=request.session['user'])
            institute = Institute.objects.get(user=user)
            
            if('delteSno' in request.POST):
                delObj = BatchTiming.objects.get(sid=request.POST.get('delteSno'))
                delObj.delete()
                messages.warning(request, "Batch Deleted Successfully")
            else:
                courseID = request.POST.get("courseName")
                forclass1 = request.POST.getlist('forclass', '')
                forclass = ', '.join(forclass1)
                batchName = request.POST.get('batchName')
                startTime = request.POST.get('startTime')
                endTime = request.POST.get('endTime')
                original = startTime+","+endTime
                try:
                    startTime = ampm(startTime)
                    endTime = ampm(endTime)
                except Exception as e:
                    print(e)
                days = request.POST.getlist('fordays')
                days = ", ".join(days)
                course = Courses.objects.get(id = courseID)
                batchObj = BatchTiming(
                    #course=Courses.objects.get(id=int(courseID[0])),
                    course=course,
                    forclass=forclass,
                    batchName=batchName,
                    startTime=startTime,
                    endTime=endTime,
                    institute=institute,
                    days=days,
                    original24time=original
                )
                batchObj.save()
                messages.success(request, "Batch Added Successfully")
        user = User.objects.get(username=request.session['user'])
        coachingCenter = Institute.objects.get(user=user).BatchTiming.all()
        inst = Institute.objects.get(user=user)
        courses = Courses.objects.filter(intitute=inst, archieved=False)
        forclass_sel = Courses.objects.filter(intitute=inst).values_list('forclass').distinct()
        jsonCources = {}
        bat = BatchTiming.objects.all()
        for x in courses:
            jsonCources[x.id] = x.forclass.split(", ")
        params = {'data': coachingCenter, 'courses': courses,'classes':forclass_sel,'bat':bat,
                  'json': json.dumps(jsonCources)}
        return render(request, 'batches/batch-timing.html', params)
    return HttpResponse("You Are not Authenticated for this Page")

def Findbatch(request):
    courses={}
    forclass = request.GET.get('forclass')
    print("forclass",forclass)

    if forclass:
        course_obj = Courses.objects.filter(forclass=forclass)
        courses = []
        for i in course_obj:
            courses.append((i.id,i.courseName))
        print('jsoncourse',courses)
    return JsonResponse({'courses':courses})


@login_required(login_url='Login')
def batchTiming(request):
    if request.session['type'] == 'Institute':
        if request.method == 'POST':
            user = User.objects.get(username=request.session['user'])
            institute = Institute.objects.get(user=user)
            if('delteSno' in request.POST):
                delObj = BatchTiming.objects.get(
                    id=request.POST.get('delteSno'))
                delObj.delete()
                messages.warning(request, "Batch Deleted Successfully")
            else:
                courseID = request.POST.get("courseName")
                forclass1 = request.POST.getlist('forclass', '')
                forclass = ', '.join(forclass1)
                batchName = request.POST.get('batchName')
                startTime = request.POST.get('startTime')
                endTime = request.POST.get('endTime')
                original = startTime+","+endTime
                try:
                    startTime = ampm(startTime)
                    endTime = ampm(endTime)
                except Exception as e:
                    print(e)
                days = request.POST.getlist('fordays')
                print('days',days)
                days = ", ".join(days)
                batchObj = BatchTiming(
                    course=Courses.objects.get(id=int(courseID[0])),
                    forclass=forclass,
                    batchName=batchName,
                    startTime=startTime,
                    endTime=endTime,
                    institute=institute,
                    days=days,
                    original24time=original
                )
                batchObj.save()
                messages.success(request, "Batch Added Successfully")
        user = User.objects.get(username=request.session['user'])
        coachingCenter = Institute.objects.get(user=user).BatchTiming.all()
        inst = Institute.objects.get(user=user)
        courses = Courses.objects.filter(intitute=inst, archieved=False)
        jsonCources = {}
        for x in courses:
            jsonCources[x.id] = x.forclass.split(", ")
        params = {'data': coachingCenter, 'courses': courses,
                  'json': json.dumps(jsonCources)}
        return render(request, 'batches/batchTiming.html', params)
    return HttpResponse("You Are not Authenticated for this Page")


@login_required(login_url="Login")
def batchTimingEdit(request, id):
    if request.session['type'] == "Institute":
        user = User.objects.get(username=request.session['user'])
        inst = Institute.objects.get(user=user)
        batchObj = BatchTiming.objects.get(id=id, institute=inst)
        forclass = Courses.objects.filter(intitute=inst).values_list('forclass').distinct()
        if request.method == "POST":
            courseName = request.POST.get("courseName")
            forclass1 = request.POST.getlist('forclass', '')
            forclass = ', '.join(forclass1)
            batchName = request.POST.get('batchName')
            startTime = request.POST.get('startTime')
            endTime = request.POST.get('endTime')
            original = startTime+","+endTime
            try:
                startTime = ampm(startTime)
                endTime = ampm(endTime)
            except Exception as e:
                print(e)
            days = request.POST.getlist('forday')
            days = ", ".join(days)
            batchObj.batchName = batchName
            batchObj.startTime = startTime        
            batchObj.courseName=courseName
            # batchObj.course = Courses.objects.get(id = courseID)
            batchObj.forclass = forclass
            batchObj.endTime = endTime
            batchObj.days = days
            batchObj.original24time = original
            batchObj.save()
            messages.success(request, "Batch Edited Successfully")
            return redirect("batchTiming2")
        courses = Courses.objects.filter(intitute=inst, archieved=False)
        jsonCources = {}
        for x in courses:
            jsonCources[x.id] = x.forclass.split(", ")
        params = {'batchObj': batchObj, 'courses': courses,'classes':forclass,
                  'json': json.dumps(jsonCources)}
        return render(request, 'batches/batchTimingEdit.html', params)
    return HttpResponse("You Are not Authenticated for this Page")

@login_required(login_url="Login")
def batchTimingdelete(request, id):
    if request.session['type'] == "Institute":
        user = User.objects.get(username=request.session['user'])
        inst = Institute.objects.get(user=user)
        batchObj = BatchTiming.objects.get(id=id)       
       # course = Courses.objects.get(id=id, intitute=inst)
        batchObj.delete()
        messages.success(request, "Batch Deleted Succssfully")
        return redirect("batchTiming2")
    return HttpResponse("You Are Not Authenticated for this Page")
        
@login_required(login_url='Login')
def postNotice(request):
    context = {}
    if request.session['type'] == "Institute":
        if request.method == "POST":
            title = request.POST.get("title")
            desc = request.POST.get("description")
            batch_name = request.POST.get("batch")
            print(request.POST)
            print('batch_name--', batch_name)
            batch = BatchTiming.objects.get(batchName=batch_name)
            newNotice = Notice(
                title=title,
                description=desc,
                batch=batch
            )
            newNotice.save()
            messages.success(request, "Notice Sent Successfully!!")
            return redirect("postNotice")
        user = User.objects.get(username=request.session['user'])
        context['batches'] = Institute.objects.get(user=user).BatchTiming.all()
        return render(request, 'batches/postNotice.html', context)
    return HttpResponse("You Are not Authenticated for this Page")


@login_required(login_url="Login")
def BatchTutor(request):
    if request.session['type'] == "Teacher":
        errors = []
        format_str = '%Y-%m-%d'
        user = User.objects.get(username=request.session['user'])
        tutor = Teacher.objects.get(user=user)
        context = {}
        if request.method == "POST":
            name = request.POST.get("batchName", "")
            starttime = request.POST.get("startTime", "")
            endtime = request.POST.get("endTime", "")
            startdate = request.POST.get("startdate", "")
            enddate = request.POST.get("enddate", "")
            forday = request.POST.getlist("forday", "")
            days = ",".join(forday)
            startdate = datetime.strptime(startdate, format_str)
            enddate = datetime.strptime(enddate, format_str)
            print(name, starttime, endtime, startdate, enddate, forday, days)
            try:
                data = BatchTimingTutor(
                    Tutor=tutor,
                    batchName=name,
                    days=days,
                    startTime=starttime,
                    endTime=endtime,
                    StartDate=startdate,
                    EndDate=enddate)
                data.save()
            except:
                errors.append("Error Occurred While processing")
        context['errors'] = errors
        if enrollTutors.objects.filter(teacher=tutor).exists():
            INSTtutor = enrollTutors.objects.get(teacher=tutor)
            context['tutor'] = INSTtutor.teachType
            inst = INSTtutor.institute
            course = INSTtutor.courseName
            course = Courses.objects.get(id=course)
            batch = BatchTiming.objects.get(course=course)
            context['INSTbatch'] = []
            context['INSTbatch'].append(batch)
        else:
            context['INSTbatch'] = []
            context['tutor'] = []
        if BatchTimingTutor.objects.filter(Tutor=tutor).exists():
            context['data'] = BatchTimingTutor.objects.filter(Tutor=tutor)
        else:
            context['data'] = []
        return render(request, 'batches/addBatchTutor.html', context)
    return HttpResponse("You Are not Authenticated for this Page")


@login_required(login_url="Login")
def editBatchTutor(request, batch_id):
    if request.session['type'] == "Teacher":
        format_str = '%Y-%m-%d'
        try:
            data = BatchTimingTutor.objects.get(sno=batch_id)
        except:
            data = []
        if request.method == "POST":
            name = request.POST.get("batchName", "")
            starttime = request.POST.get("startTime", "")
            endtime = request.POST.get("endTime", "")
            startdate = request.POST.get("startdate", "")
            enddate = request.POST.get("enddate", "")
            forday = request.POST.getlist("forday", "")
            days = ",".join(forday)
            startdate = datetime.strptime(startdate, format_str)
            enddate = datetime.strptime(enddate, format_str)
            print(name, starttime, endtime, startdate, enddate, forday, days)
            if name:
                data.batchName = name
            if starttime:
                data.startTime = starttime
            if endtime:
                data.endTime = endtime
            if startdate:
                data.StartDate = startdate
            if enddate:
                data.EndDate = enddate
            if forday:
                data.days = days
            data.save()
            return redirect('addbatchtutor')
        context = {
            'data': data
        }
        return render(request, 'batches/editBatchTutor.html', context)
    return HttpResponse("You Are not Authenticated for this Page")


@login_required(login_url="Login")
def deleteBatchTutor(request, batch_id):
    if request.session['type'] == "Teacher":
        errors = []
        try:
            data = BatchTimingTutor.objects.get(sno=batch_id)
            data.delete()
            return redirect('addbatchtutor')
        except:
            errors.append('Error Occured')
        context = {
            'errors': errors
        }
        return render(request, 'batches/addBatchTutor.html', context)
    return HttpResponse("You Are not Authenticated for this Page")
