from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from accounts.models import Institute, Teacher, Student, Tutorid
from django.core.files.base import ContentFile
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from .models import OTP
from batches.models import BatchTiming
from django.contrib.auth.models import User
import math
import random
from django.contrib import auth
from django.core.mail import EmailMessage
from django.contrib import messages
from accounts.models import *
from courses.models import *
from teacher.models import *
from students.models import *
from json import dumps, loads
import json

@login_required(login_url='Login')
def dashboard2(request):
    if request.session['type'] == "Institute":
        return render(request, "dashboard-2/dashboard.html")


@login_required(login_url='Login')
def dashboard(request):
    if request.session['type'] == "Institute":
        inst = Institute.objects.get(user=User.objects.get(username=request.session['user']))
        course_count = Courses.objects.filter(intitute=inst).count()
        tutor_count = len(enrollTutors.objects.filter(institute=inst).values_list('teacher').distinct())
        student_count = len(AddStudentInst.objects.filter(institute=inst).values_list('student').distinct())
        all_events = BatchTiming.objects.all()
        
        context = {
            "course_count" : course_count,
            "tutor_count" : tutor_count,
            "student_count" : student_count,      
            "events":all_events   }
        return render(request, "dashboard/institute-dashboard.html",context)
    elif request.session['type'] == "Teacher":
        user = User.objects.get(username=request.session['user'])
        teacher = Teacher.objects.get(user=user)
        if teacher.course == "None" or teacher.qualification == "None" or teacher.experiance == -1:
            return redirect("signupTutorContinued", teacher.id)
        else:
            # return render(request, "dashboard/Tutor-dashboard.html")
            template = 'dashboard/Tutor-dashboard.html'    
            makepoint = MakeAppointment.objects.all()
            return render(request,'teacher/teachercalendar.html',{'template':template,'makepoint':makepoint})
    elif request.session['type'] == "Student":
        # return render(request, "dashboard/student-dashboard.html")
        template = 'dashboard/student-dashboard.html' 
        makepoint = MakeAppointment.objects.all()
        return render(request,'students/studentcalendar.html',{'template':template,'makepoint':makepoint})

@login_required(login_url='Login')
def profileUpdate(request):
    if request.session['type'] == 'Institute' or request.session['type'] == 'Teacher' or request.session['type'] == 'Student':
        user = User.objects.get(username=request.session['user'])
        combinedZip = []
        doc = []
        if request.session['type'] == "Institute":
            my_template = 'dashboard/base.html'
            obj = Institute.objects.get(user=user)
        elif request.session['type'] == "Teacher":
            my_template = 'dashboard/Tutor-dashboard.html'
            obj = Teacher.objects.get(user=user)
            doc = Tutorid.objects.get(teacherid = obj.id)

            classcoursefees = []
            teach = []
            classList = obj.forclass.split(',')
            courseList = obj.course.split(',')
            teachList = obj.teachType.split(',')
            feesList = obj.fees.split(',')

            for i in range(len(classList)):
                x = (classList[i],courseList[i],feesList[i])
                if x not in classcoursefees:
                    classcoursefees.append(x)
                    teach.append([teachList[i]])
                else:
                    teach[-1].append(teachList[i])

            classList,courseList,feesList = list(zip(*classcoursefees))
            combinedZip = list(zip(classList,courseList,teach,feesList))

        else:
            if request.session['type'] == "Student":
                my_template = 'dashboard/student-dashboard.html'
                obj = Student.objects.get(user=user)
        if request.method == "POST":
            if 'otpReceived' in request.POST:
                otp = request.POST.get('otp')
                email = request.POST.get('email')
                otp_obj = OTP.objects.get(type='any', user=email)
                if (inst.email == email) and otp_obj:
                    if otp_obj.otp == otp:
                        inst.emailValidated = True
                        inst.save()
                otp_obj.delete()
                return redirect('coachingprofile')
            else:
                phone = request.POST.get('phone')
                email = request.POST.get('email')
                address = request.POST.get('loc')
                # avatar = request.POST.get('avatar',0)
                error = 0
                if(not phone.isdigit()):
                    messages.warning(
                        request, "Phone number should be numeric.")
                    error = 1
                if(len(phone) != 10):
                    messages.warning(
                        request, "Phone number should be 10 digits long.")
                    error = 1
                if(error == 0):
                    if request.session['type'] == "Institute":
                        latitude = request.POST.get('cityLat')
                        longitude = request.POST.get('cityLng')
                        obj = Institute.objects.get(user=user)
                        obj.phone = phone
                        obj.latitude = latitude
                        obj.longitude = longitude
                        obj.address = address
                        obj.save()
                        auth.login(request, user)
                        request.session["user"] = user.username
                        request.session["type"] = "Institute"
                    elif request.session['type'] == "Teacher":
                        qualification = request.POST.get('qualification')
                        experience = request.POST.get('experience')
                        subject = request.POST.get('subject')
                        obj = Teacher.objects.get(user=user)
                        obj.phone = phone
                        obj.experiance = experience
                        obj.qualification = qualification
                        obj.subject = subject
                        obj.address = address
                        obj.save()
                        auth.login(request, user)
                        request.session["user"] = user.username
                        request.session["type"] = "Teacher"
                    elif request.session['type'] == "Student":
                        schoolName = request.POST.get('schoolName')
                        qualification = request.POST.get('qualification')
                        obj = Student.objects.get(user=user)
                        obj.phone = phone
                        obj.qualification = qualification
                        obj.schoolName = schoolName
                        obj.address = address
                        obj.save()
                        auth.login(request, user)
                        request.session["user"] = user.username
                        request.session["type"] = "Student"
                    messages.success(request, "Profile Upated Succsefully")
        with open('cc.txt') as f:
            data = f.read()         
            data = json.loads(data)
            f.close()
        return render(request, "dashboard/profileCoachingCentre.html",{'centre': obj, 'my_template': my_template,'combinedZip':combinedZip,'doc':doc,'data':data})
    return HttpResponse("You are not Authenticated for this page")

def picChange(request):
    if request.session['type'] == "Institute" or request.session['type'] == "Teacher" or request.session['type'] == "Student":
        user = User.objects.get(username=request.session['user'])
        image = request.FILES.get('photo')
        if request.session['type'] == "Institute":
            obj = Institute.objects.get(user=user)
        elif request.session['type'] == "Teacher":
            obj = Teacher.objects.get(user=user)
        elif request.session['type'] == "Student":
            obj = Student.objects.get(user=user)
        if image:
            obj.photo = image
            obj.save()
        messages.success(request, "Profile Picture Upated Succsefully")
        return redirect('coachingprofile')
    return HttpResponse("You are not Authenticated for this page")

def changePassword(request):
    user = User.objects.get(username=request.session['user'])

    if request.session['type'] == "Institute" or request.session['type'] == "Teacher" or request.session['type'] == "Student":
        if request.session['type'] == "Institute":
            template = 'dashboard/base.html'
            obj = Institute.objects.get(user=user)
        elif request.session['type'] == "Teacher":
            template = 'dashboard/Tutor-dashboard.html'
            obj = Teacher.objects.get(user=user)
        elif request.session['type'] == "Student":
            template = 'dashboard/student-dashboard.html'
            obj = Student.objects.get(user=user)

        if request.method == "POST":
            oldPassword = request.POST.get('oldPassword')
            newPassword = request.POST.get('newPassword')
            confPassword = request.POST.get('confirmPassword')

            if(oldPassword != obj.user.password):
                messages.warning(request, "Incorrect Password! Please Enter Correct Password.")
            if(len(newPassword) < 3 or len(newPassword) > 20):
                messages.warning(request, "Password length should be between 3 and 20")
            if(newPassword != confPassword):
                messages.warning(request, "New Password and Confirm Password does not match")
                
            obj.password = newPassword
            obj.save()
            messages.success(request, "Password Succesfully Changed")

        return render(request, "dashboard/changePassword.html", {'template': template})

    return HttpResponse("You are not Authenticated for this page")

def updateClasses(request):
    teacher = Teacher.objects.get(user=User.objects.get(username=request.session['user']))
    classList,courseList,teachList,feesList = mapClassCourse(request.POST.getlist('class'), request.POST.getlist('course'), request.POST.getlist('teach'), request.POST.getlist('fees'))
    teacher.forclass = classList
    teacher.course = courseList
    teacher.teachType = teachList
    teacher.fees = feesList
    teacher.save()
    messages.success(request, "Classes Updated Succsefully")
    return redirect('coachingprofile')

def updateDocs(request):
    teacher = Teacher.objects.get(user=User.objects.get(username=request.session['user']))
    tutorid = Tutorid.objects.get(teacherid=teacher.id,teachername=teacher)
    tutorid.panaadhar = request.POST.get('idcard')
    tutorid.panaadharnumber = request.POST.get('idnum')
    photoid = request.FILES.get('idimg') 
    if photoid:
        tutorid.photoid = photoid
    tutorid.save()
    messages.success(request, "Personal Details Updated Succsefully")
    return redirect('coachingprofile')

def getOTP(request):
    if request.method == "POST":
        email = request.POST.get('email')
        if email:
            digits = "0123456789"
            otp_code = ""
            for i in range(8):
                otp_code += digits[math.floor(random.random() * 10)]
            # send OTP EMAIL
            email2 = 'gkdevtest777@gmail.com'
            msg = EmailMessage(
                'Validate Email', "Your OTP for validating Email is "+str(otp_code), email2, to=[email])
            msg.send()
            type = 'any'
            otp = OTP(
                otp=otp_code,
                user=email,
                type=type
            )
            return JsonResponse({'status': 1})
        else:
            return JsonResponse({'status': 0})

def mapClassCourse(classList, courseList, teachList, feesList):
    five_subj = ["English", "Maths", "Science", "Evs", "Hindi"]

    classcourseteach = []
    combinedList = []

    for i in range(len(classList)):
        x = (classList[i],courseList[i],teachList[i])
        y = (classList[i],courseList[i],teachList[i],feesList[i])
        if x not in classcourseteach:
            classcourseteach.append(x)
            combinedList.append(y)

    Other = []
    Nursery = []
    combinedSet = []

    for i in range(len(combinedList)):
        if combinedList[i][0]=='Other':
            Other.append(combinedList[i])

        elif combinedList[i][0]=='Nursery' and combinedList[i][1]=='All Subjects':
            for j in range(len(five_subj)):
                Nursery.append((combinedList[i][0],five_subj[j],combinedList[i][2],combinedList[i][3])) 

        elif combinedList[i][0]=='Nursery' and combinedList[i][1]!='All Subjects':
            Nursery.append(combinedList[i])

        elif combinedList[i][0]!='Nursery' and combinedList[i][1]=='All Subjects':
            for j in range(len(five_subj)):
                combinedSet.append((combinedList[i][0],five_subj[j],combinedList[i][2],combinedList[i][3]))  

        else:
            combinedSet.append(combinedList[i])

    combinedList = combinedSet
    combinedList = sorted(list(set(combinedList)),key = lambda x: int(x[0]))
    OtherList = sorted(list(set(Other)),key = lambda x: x[1])
    NurseryList = sorted(list(set(Nursery)),key = lambda x: x[1])

    classList,courseList,teachList,feesList = list(zip(*(NurseryList + combinedList + OtherList)))
    classList,courseList,teachList,feesList = ','.join(classList),','.join(courseList),','.join(teachList),','.join(feesList)
    
    return classList,courseList,teachList,feesList

@login_required(login_url="Login")
def signupTutorContinued(request, id):
    if request.session['type'] == "Teacher":
        if request.method == 'POST':
            teacher = Teacher.objects.get(id=id)
            
            teacher.experiance = request.POST.get('experience')
            teacher.qualification = request.POST.get('qualification')
            teacher.desc = request.POST.get('description')

            if request.POST.get('demo')=="1":
                teacher.democlass = True

            classList,courseList,teachList,feesList = mapClassCourse(request.POST.getlist('class'), request.POST.getlist('course'), request.POST.getlist('teach'), request.POST.getlist('fees'))

            teacher.forclass = classList
            teacher.course = courseList
            teacher.teachType = teachList
            teacher.fees = feesList

            image = request.FILES.get('photo')

            if image:
                teacher.photo = image
            teacher.save()

            teacher.gender = request.POST.get('gender')
            teacher.address = request.POST.get('address')
            tutorid,created = Tutorid.objects.get_or_create(teacherid=id,teachername=teacher)
            tutorid.panaadhar = request.POST.get('idcard')
            tutorid.panaadharnumber = request.POST.get('idnum') 
            tutorid.photoid = request.FILES.get('idimg') 
            tutorid.save()
            return redirect('dashboard')

        with open('cc.txt') as f:
            data = f.read()         
            data = json.loads(data)
            f.close()

        return render(request,'dashboard/signupTutorContinued.html',{"data": data})
    return HttpResponse("You are not Authenticated for this page")
