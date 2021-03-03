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

# Create your views here.


@login_required(login_url='Login')
def courses(request):
    with open('cc.txt') as f:
        data = f.read()         
    data = json.loads(data)
    
    if request.session['type'] == "Institute":
        user = User.objects.get(username=request.session['user'])
        inst = Institute.objects.get(user=user)
        courses = Courses.objects.filter(intitute = inst)
       # courses = Courses.objects.all()
       # courses = Courses.objects.filter(intitute = inst)
       # courses = Courses.objects.all()
        
        # paginator = Paginator(courses, 4)
        # page = request.GET.get('page', 1)
        # try:
        #     course = paginator.page(page)
        # except PageNotAnInteger:
        #     course = paginator.page(1)
        # except EmptyPage:
        #     course = paginator.page(paginator.num_pages)
        # print(courses)
        params = {'course': courses,'data':data}

        if request.method == "POST":
            courseName = request.POST.get('courseName') 
            print('coursename',courseName)           
            forclass = request.POST.get('forclass')           
           # forclass = ', '.join(forclass)            
           # courseName = ','.join(forclass)
            print('courseName',courseName)           
            user = User.objects.get( username=request.session['user'])            
            institute = Institute.objects.get(user=user)
            count = (Courses.objects.all().count())+1 
            course_ID = courseName[:3] + str("%03d" % count)
            if  not Courses.objects.filter(courseName=request.POST['courseName']).exists():
                if not Courses.objects.filter(forclass=request.POST['forclass']).exists():
                    
                    print('if else coursename',courseName)  
                    print('if else for class',forclass)  
                    Courses(courseName=courseName,
                     forclass=forclass,
                     intitute=institute,
                     courseID=course_ID).save()
                    messages.success(request, 'Course Has been added successfully.')
                    return redirect('courses')
                    
                else:
                    messages.warning(request, 'class Number Already Exists!!! ',extra_tags = 'alert alert-warning alert-dismissible show')
            else:
                messages.warning(request, 'Course Already Exists!!! ',extra_tags = 'alert alert-warning alert-dismissible show')            
   

            #Added coursse
            # Courses(courseName=courseName,
            #          forclass=forclass,
            #          intitute=institute,
            #          courseID=course_ID).save()
            # messages.success(request,"Course Added Successfully")
            # return redirect('courses')

            # Courses(courseName=courseName,
            #          forclass=forclass,
            #          intitute=institute,
            #          courseID=course_ID).save()
            # messages.success(request,"Course Added Successfully")
            # return redirect('courses')
        return render(request, 'courses-2/courses.html', params)
    return HttpResponse("You Are Not Authenticated for this Page")


@login_required(login_url='Login')
def courseArchive(request):
    if request.session['type'] == "Institute":
        user = User.objects.get(username=request.session['user'])
        inst = Institute.objects.get(user=user)

        if(request.method == 'POST'):
            undo = request.POST.getlist('undo')
            for id in undo:
                course = Courses.objects.get(id=int(id))
                course.archieved = False
                course.save()
            messages.success(
                request, "Courses Removed from Archive Successfully")
            return redirect("courseArchive")
        courses = Courses.objects.filter(intitute=inst, archieved=True)
        paginator = Paginator(courses, 4)
        page = request.GET.get('page', 1)
        try:
            course = paginator.page(page)
        except PageNotAnInteger:
            course = paginator.page(1)
        except EmptyPage:
            course = paginator.page(paginator.num_pages)
        params = {'course': courses}
        return render(request, 'courses-2/archive-courses.html', params)
    return HttpResponse("You Are Not Authenticated for this Page")


@login_required(login_url='Login')
def teachingType2(request):
    if request.session['type'] == "Institute": 
        user = User.objects.get(username=request.session['user'])
        inst = Institute.objects.get(user=user)
        courses = Courses.objects.filter(intitute=inst)   
        print('courses',courses)       
        jsonCources = {}       
        for x in courses:
            jsonCources[x.id] = x.forclass.split(", ")
        print('jsonCources ',jsonCources)
        classes = dict()
        for i in courses:
            classes[i.pk] = i.forclass
        print('classes',classes)
        teach = TeachingType.objects.filter(course__intitute = inst)
        paginator = Paginator(teach, 10)
        page = request.GET.get('page', 1)
        try:
            teach = paginator.page(page)
        except PageNotAnInteger:
            teach = paginator.page(1)
        except EmptyPage:
            teach = paginator.page(paginator.num_pages)
        params = {'teach': teach, 
                  'courses': courses,
                  'classes': classes, 
                  'json': json.dumps(jsonCources)}

        if request.method == "POST":
            print('requestPost',request.POST)

            courseID = request.POST.get('courseName')

            forclass1 = request.POST.getlist('forclass', '')
            forclass = ', '.join(forclass1)
            teachType1 = request.POST.getlist('check')
            teachType = '\n'.join(teachType1)
            print('teachtype',teachType1)
            duration1 = request.POST.getlist('duration', '')
            duration = '\n'.join(duration1)
            timePeriod1 = request.POST.getlist('time', '')
            timePeriod = '\n'.join(timePeriod1)




            alreadyExists = TeachingType.objects.filter(courseID = courseID, forclass = forclass,                                           
                                                        teachType = teachType,
                                                         duration = duration, 
                                                         timePeriod = timePeriod)


            if(alreadyExists):
                return HttpResponse("""
						<script>
							alert('Teach Type already exists');
							window.location.href = "/teachingType2";
						</script>
					""")
      
            #course = Courses.objects.get(id = int(courseID[0]))
            course = Courses.objects.get(id = courseID)
                       
            print('course--', course)
            teachingtype = TeachingType(course =course, 
                                         courseID=int(courseID),
                                         forclass=forclass, 
                                         teachType=teachType,
                                          duration=duration,                                         
                                           timePeriod=timePeriod)
            teachingtype.save()
            messages.success(request, "Teaching type Added Successfully")
            return redirect('teaching-type-2')
        return render(request, 'courses-2/teaching-type.html', params)
    return HttpResponse("You Are Not Authenticated for this Page")

# @login_required(login_url='Login')
# def couse_delete(request, pk):
#     if request.session['type'] == "Institute": 
#         user = User.objects.get(username=request.session['user'])
#         inst = Institute.objects.get(user=user)
#         course = Couse.objects.get(id=pk)
#         course.delete()
#         return redirect("course")
#     return HttpResponse("You Are Not Authenticated for this Page")





@login_required(login_url='Login')
def addCourses(request):
    if request.session['type'] == "Institute":
        if request.method == "POST":
            courseName = request.POST.get('courseName')
            forclass = request.POST.getlist('forclass')
            forclass = ', '.join(forclass)
            user = User.objects.get(username=request.session['user'])
            institute = Institute.objects.get(user=user)
            count = (Courses.objects.all().count())+1
            course_ID = courseName[:3] + str("%03d" % count)
            Courses(courseName=courseName, forclass=forclass,
                    intitute=institute, courseID=course_ID).save()
            messages.success(request, "Course Added Successfully")
            return render(request, 'courses/addCourses.html')
        return render(request, 'courses/addCourses.html')
    return HttpResponse("You Are Not Authenticated for this Page")


@login_required(login_url='Login')
def viewCourses(request):
    if request.session['type'] == "Institute":
        user = User.objects.get(username=request.session['user'])
        inst = Institute.objects.get(user=user)
        courses = Courses.objects.filter(intitute=inst, archieved=False)
        print(courses)
        params = {'courses': courses}
        if request.method == "POST":
            check = request.POST.getlist('check')
            for id in check:
                course = Courses.objects.get(id=int(id))
                course.archieved = True
                course.save()
            messages.success(request, "Courses Added to Archive Successfully")
            return redirect("viewCourses")
        return render(request, 'courses/viewCourses.html', params)
    return HttpResponse("You Are Not Authenticated for this Page")


@login_required(login_url='Login')
def archiveCourseList(request):
    if request.session['type'] == "Institute":
        user = User.objects.get(username=request.session['user'])
        inst = Institute.objects.get(user=user)
        if(request.method == 'POST'):
            undo = request.POST.getlist('undo')
            print('undo',undo)
            for id in undo:
                course = Courses.objects.get(id=int(id))
                course.archieved = False
                course.save()
            messages.success(
                request, "Courses Removed from Archive Successfully")
            return redirect("archiveCourseList")
        courses = Courses.objects.filter(intitute=inst, archieved=True)
        params = {'course': courses}
        return render(request, 'courses/archiveCourseList.html', params)
    return HttpResponse("You Are Not Authenticated for this Page")


# @login_required(login_url="Login")
# def deleteCourse(request, id):
#     if request.session['type'] == "Institute":
#         user = User.objects.get(username=request.session['user'])
#         inst = Institute.objects.get(user=user)
#         course = Courses.objects.get(id=id, intitute = inst ) 
#         course.delete()
#         messages.success(request, "Course Deleted Succssfully")
#         return redirect("courses")
#     return HttpResponse("You Are Not Authenticated for this Page")


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

@login_required(login_url="Login")
def deleteteaching(request, id):
    if request.session['type'] == "Institute":
        user = User.objects.get(username=request.session['user'])
        inst = Institute.objects.get(user=user)
        course = TeachingType.objects.get(id=id)
        course.delete()
        messages.success(request, "Teaching Type Deleted Succssfully")
        return redirect("teaching-type-2")
    return HttpResponse("You Are Not Authenticated for this Page")

@login_required(login_url="Login")
def editCourse(request, id):
    if request.session['type'] == "Institute":
        user = User.objects.get(username=request.session['user'])
        inst = Institute.objects.get(user=user)
        course = Courses.objects.get(id=id, intitute=inst)
        classes = course.forclass.split(', ')

        params = {'course': course.courseName, 'class': classes}

        if request.method == "POST":
            courseName = request.POST.get('editcourseName', '')
            print('editcourseName',courseName)

            forclass = request.POST.getlist('forclass', '')

            print('editforclass',forclass)
            forclass = ', '.join(forclass)
            course.courseName = courseName
            course.forclass = forclass
            course.save()
            messages.success(request, "Course Updated Successfully")
            return redirect("courses")
        return render(request, 'courses/editCourse.html', params)
    return HttpResponse("You Are Not Authenticated for this Page")


@login_required(login_url='Login')
def teachingType(request):
    if request.session['type'] == "Institute":
        user = User.objects.get(username=request.session['user'])
        inst = Institute.objects.get(user=user)
        courses = Courses.objects.filter(intitute=inst)
        jsonCources = {}
        for x in courses:
            jsonCources[x.id] = x.forclass.split(", ")
        params = {'courses': courses, 'json': json.dumps(jsonCources)}
        if request.method == "POST":
            print('requestpost',request.POST)
               
            courseID = request.POST.get('courseName')
            forclass1 = request.POST.getlist('forclass', '')
            forclass = ', '.join(forclass1)
            teachType1 = request.POST.getlist('check')
            teachType = '\n'.join(teachType1)
            duration1 = request.POST.getlist('duration', '')
            duration = '\n'.join(duration1)
            timePeriod1 = request.POST.getlist('time', '')
            timePeriod = '\n'.join(timePeriod1)
            alreadyExists = TeachingType.objects.filter(courseID=int(courseID),
                                                          forclass=forclass,
                                                           teachType=teachType,
                                                            duration=duration,
                                                             timePeriod=timePeriod)
            if(alreadyExists):
                return HttpResponse("""
						<script>
							alert('Teach Type already exists');
							window.location.href = "/teachingType";
						</script>
					""")
            course = Courses.objects.get(id=int(courseID[0]))
            print('course--', course)
            teachingtype = TeachingType(course=course, courseID=int(
                courseID), forclass=forclass, teachType=teachType, duration=duration, timePeriod=timePeriod)
            teachingtype.save()
            messages.success(request, "Teaching type Added Successfully")
            return redirect('viewteachType')
        return render(request, 'courses/teachingType.html', params)
    return HttpResponse("You Are Not Authenticated for this Page")


@login_required(login_url='Login')
def viewteachType(request):
    if request.session['type'] == "Institute":
        user = User.objects.get(username=request.session['user'])
        inst = Institute.objects.get(user=user)
        teach = TeachingType.objects.filter(course__intitute=inst)
        params = {'teach': teach}
        return render(request, 'courses/viewteachType.html', params)
    return HttpResponse("You Are Not Authenticated for this Page")


@login_required(login_url="Login")
def editTeachingType(request, id):
    if request.session['type'] == "Institute":
        user = User.objects.get(username=request.session['user'])
        inst = Institute.objects.get(user=user)
        courses = Courses.objects.filter(intitute=inst)
        teach = TeachingType.objects.get(id=id)
        classes = teach.course.forclass.split(', ')
        courseID = int(teach.courseID)
        params = {'teach': teach, 'courses': courses,
                  'courseID': courseID, 'classes': classes}
        if request.method == "POST":
            print(request.POST)
            courseID = request.POST.get('courseName')
            forclass1 = request.POST.getlist('forclass', '')
            forclass = ','.join(forclass1)
            teachType1 = request.POST.getlist('check')
            teachType = '\n'.join(teachType1)
            duration1 = request.POST.getlist('duration', '')
            duration = '\n'.join(duration1)
            print(duration)
            timePeriod1 = request.POST.getlist('time', '')
            timePeriod = '\n'.join(timePeriod1)
            print(timePeriod)
            #course = Courses.objects.get(id=int(courseID[0]))
            course = Courses.objects.get(id = courseID)
            teach.course = course
            teach.courseID = int(courseID)
            teach.forclass = forclass
            teach.teachType = teachType
            teach.duration = duration
            teach.timePeriod = timePeriod
            teach.save()
            messages.success(request, 'Teaching Type Edited Successfully')
            return redirect('viewteachType')
        return render(request, 'courses/editTeachingType.html', params)
    return HttpResponse("You Are Not Authenticated for this Page")
