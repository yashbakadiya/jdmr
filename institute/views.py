from django.shortcuts import render,HttpResponseRedirect,HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from teacher.models import enrollTutors
from students.models import AddStudentInst
from accounts.models import Teacher,Student,Institute
from django.contrib import messages
from .models import *
from courses.models import Courses
from django.db.models import Q
from batches.models import BatchTiming
from json import loads
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.
@login_required(login_url="Login")
def instituteTutor(request):
    if request.session['type']=="Teacher" or request.session['type']=="Student":
        if request.session['type']=="Teacher":
            user = User.objects.get(username=request.session['user'])
            tutor = Teacher.objects.get(user=user)
            if enrollTutors.objects.filter(teacher=tutor).exists():
                INST = enrollTutors.objects.filter(teacher=tutor)
                courses = []
                for ins in INST:
                    course = Courses.objects.get(id= int(ins.courseName))
                    courses.append(course)
                batches = zip(INST,courses)
                return render(request,"Institute/institute.html",{"INST":INST[0],"batches":batches,"template":"dashboard/Tutor-dashboard.html"})
            else:
                messages.warning(request,"Not Found")
                return render(request,"Institute/institute.html",{"template":"dashboard/Tutor-dashboard.html"})
        elif request.session['type']=="Student":
            user = User.objects.get(username=request.session['user'])
            student = Student.objects.get(user=user)
            if AddStudentInst.objects.filter(student=student).exists():
                INST = AddStudentInst.objects.filter(student=student)
                batches = []
                for ins in INST:
                    batch = BatchTiming.objects.get(id= int(ins.batch))
                    batches.append(batch)
                print('stuent fees-',student.fees.all)
                return render(request,"Institute/institute.html",{"batches":batches,'student':student,"INST":INST[0],"template":"dashboard/student-dashboard.html"})
            else:
                messages.warning(request,"Not Found")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return HttpResponse("You are not Authenticated for this Page")



@login_required(login_url="Login")
def searchCoachingCenter(request):
    classlist = ['I','II','III','IV','V','VI','VII','VIII','IX','X','XI','XII','Not Applicable','Nursery']
    prefill={}
    if request.session['type']=="Student":
        centers = []
        if request.method == "POST":
            address = request.POST.get('loc','')
            distance = request.POST.get('distance','')
            cityLat = request.POST.get('cityLat','')
            cityLng = request.POST.get('cityLng','')
            Class = request.POST.get('className','')
            course = request.POST.get('subject','')
            centers = Institute.objects.filter(Q(address__icontains=address) or Q(latitude=cityLat) or Q(longitude=cityLng))
            courses = Courses.objects.filter(Q(forclass=Class) or Q(courseName__icontains=course))
            centers2 = []
            prefill = {
                    "address":address,
                    "distance":distance,
                    "class":Class,
                    "course":course
            }
            for cou in courses:
                inst = cou.intitute
                if inst not in centers2 and inst not in centers:
                    centers2.append(inst)
            # centers = zip(courses,centers2)
            return render(request, 'Institute/searchCoachingCenter.html',{'centers2':centers2,'centers':centers,'courses':Courses.objects.all(),'classes':classlist,"prefill":prefill})
        return render(request, 'Institute/searchCoachingCenter.html',{'centers':centers,'courses':Courses.objects.all(),'classes':classlist,"prefill":prefill})



@login_required(login_url="Login")
def ReviewInstitute(request,inst_id):
    user = User.objects.get(username=request.session['user'])
    user_type = request.session['type']
    show = False
    if user_type == 'Student':
        student = Student.objects.get(user=user)
        if request.method == "POST" and not(InstituteRatings.objects.filter(student=student).exists()):
            rating =request.POST.get("rating","")
            comment = request.POST.get("comment","")
            print(rating,comment)
            data = InstituteRatings(
                    institute=institute,
                    student=student,
                    Review=comment,
                    Rating =rating)
            data.save()
        template = "dashboard/student-dashboard.html"
        if not InstituteRatings.objects.filter(student=student).exists():
            show = True
    if user_type == 'Teacher':
        teacher = Teacher.objects.get(user=user)
        template = "dashboard/Tutor-dashboard.html"
    if user_type == 'Institute':
        inst = Institute.objects.get(user=user)
        template = "dashboard/institute-dashboard.html"
    institute = Institute.objects.get(id=inst_id)
    INST = InstituteRatings.objects.filter(institute=institute)
    courses = Courses.objects.filter(intitute=institute, archieved=False)
    paginator = Paginator(courses, 4)
    page = request.GET.get('page', 1)
    try:
        course = paginator.page(page)
    except PageNotAnInteger:
        course = paginator.page(1)
    except EmptyPage:
        course = paginator.page(paginator.num_pages)
    count = INST.count()
    sumRating = 0
    for i in INST:
        add = i.Rating
        sumRating+=add
    avgRating = sumRating/count
    reviews = InstituteRatings.objects.filter(institute=institute)
    context = {
        'reviews':reviews,
        'i':institute,
        'avgRating':range(int(avgRating)),
        'show':show,
        'course':course,
        'template':template
        }
    return render(request,'Institute/Reviewsinstitute.html',context)
        