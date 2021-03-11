from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.decorators import login_required
from accounts.models import Institute,Teacher,Student
from django.contrib import messages
from courses.models import TeachingType,Courses
from batches.models import BatchTiming
from .models import AddStudentInst,School,PostTution,PostAssignment
from django.contrib.auth.models import User
from json import dumps
from django.core.serializers.json import DjangoJSONEncoder
from django.forms.models import model_to_dict
import json
from django.db.models import Q
from json import dumps,loads 
import os
from math import radians, sin, cos, asin, sqrt
from geopy.geocoders import Nominatim
from get_notice import notice
from batches.models import Notice
# Create your views here.


@login_required(login_url="Login")
def stuShowAllNotice(request):
    notices = notice(request)
    return render(request, "batches/stu_showAllNotice.html", context={"notices":notices})

@login_required(login_url="Login")
def stuShowNotice(request, id):
    notice = Notice.objects.get(id=id)
    return render(request, "batches/stu_showNotice.html", context={"notice":notice})


@login_required(login_url="Login")
def addStudents(request):
    if request.session['type'] == "Institute":
        user = User.objects.get(username=request.session['user'])
        inst = Institute.objects.get(user=user)
        if request.method=="POST":
            firstName = request.POST.get('firstName', '')
            lastName = request.POST.get('lastName', '')
            email = request.POST.get('email', '')
            username = email
            phone = request.POST.get('phone', '')
            password = phone
            schoolName = request.POST.get('schoolName', '')
            lat = request.POST.get('cityLat', 1)
            lng = request.POST.get('cityLng', 1)
            if firstName.isalpha() == False | lastName.isalpha() == False | schoolName.isalpha() == False:
                messages.warning(request, "Name must be alphabetical")
                return redirect('addStudents')
            if len(phone) != 10:
                messages.warning(request, "Phone Number must be 10 digits")
                return redirect('addStudents')
            if Student.objects.filter(user__email=email).exists():
                messages.warning(request, "Student with This Email Exists")
                return redirect('addStudents')
            if Student.objects.filter(phone=phone).exists():
                messages.warning(request, "Phone Number is Already Registered")
                return redirect('addStudents')

            user = User(
                username=username,
                first_name=firstName,
                last_name=lastName,
                email=email,
                password=password,
            )
            user.save()
            student = Student(user=user,phone=phone,address=schoolName,schoolName=schoolName)
            student.save()
            if School.objects.filter(name=schoolName).exists():
                pass
            else:
                school = School(name=schoolName)
                school.save()
            # ctn = request.POST.getlist('ctn_combined')
            # cn = request.POST.getlist('cn_combined')
            # ttn = request.POST.getlist('ttn_combined')
            # ttn = [x.replace("\r","") for x in ttn]
            # batchName = request.POST.getlist('batchN_combined')
            # feeDis = request.POST.getlist('feedis_combined')
            # installments = request.POST.getlist('noi_combined')

            ctn = request.POST.getlist('ctn')
            cn = request.POST.getlist('cn')
            ttn = request.POST.getlist('ttn')
            batchName = request.POST.getlist('batchN')
            feeDis = request.POST.getlist('feedis')
            installments = request.POST.getlist('noi')
            for x in range(len(ttn)):
                try:
                    temp = float(feeDis[x])
                except:
                    try:
                        temp = int(feeDis[x])
                    except:
                        temp = 0
                addstudent = AddStudentInst(
                        student=student,
                        institute=inst,
                        courseName = ctn[x] ,
                        forclass = cn[x] ,
                        teachType = ttn[x] ,
                        batch = batchName[x],
                        feeDisc = temp,
                        installments=installments[x]
                    )
                addstudent.save()
            return redirect('viewStudents')
        schools = School.objects.all()
        school_list = list(map(str,schools))
        # data = TeachingType.objects.filter(course__intitute__user=user).values_list('courseID','forclass','teachType','course')
        # print('data--',data)
        # processed_data = {}
        # for x in data:
        #     processed_data[x[0]] = [x[1].split(", "),x[2].split("\n")]
        return render(
            request,
            'students/addStudents.html',
            {
                "data":TeachingType.objects.filter(course__intitute=inst).values_list('forclass').distinct(),
                "school_list":school_list,
                'batch':BatchTiming.objects.filter(institute=inst)
            }
        )
    return HttpResponse("You are not Authenticated for This Page")



@login_required(login_url="Login")
def viewStudents(request):
    if request.session["type"] == "Institute" :
        user = User.objects.get(username=request.session['user'])
        inst = Institute.objects.get(user=user)
        if request.method == "POST":
            check = request.POST.getlist('check')
            for x in check:
                arStudent = AddStudentInst.objects.get(id = int(x))
                arStudent.archieved = True
                arStudent.save()
            messages.success(request,"Student Added To Archieve Successfully")
            return redirect('viewStudents')
        students = AddStudentInst.objects.filter(institute=inst,archieved=False)
        courses = []
        for student in students:
            course = Courses.objects.get(courseName=student.courseName)
            courses.append(course)
        students = zip(students,courses)
        params = {'students':students}
        return render(request, 'students/viewStudents.html', params)
    return HttpResponse("You are not Authenticated for This Page")



@login_required(login_url="Login")
def deleteStudent(request,id):
    if request.session['type'] == "Institute":
        try:
            delStu = AddStudentInst.objects.get(id=id)
            delStu.delete()
            messages.warning(request,"Student Deleted Successfully")
            return redirect("viewStudents")
        except:
            messages.warning(request,"Student Id Does Not Exist")
            return redirect("viewStudents")
    return HttpResponse("You are not Authenticated for This Page")



def archiveStudentList(request):
    if request.session['type'] == "Institute":
        user = User.objects.get(username=request.session["user"])
        inst = Institute.objects.get(user=user)
        if request.method == "POST":
            check = request.POST.getlist('check')
            for x in check:
                arStudent = AddStudentInst.objects.get(id = int(x))
                arStudent.archieved = False
                arStudent.save()
            messages.success(request,"Student Removed From Archieve Successfully")
            return redirect('archiveStudentList')
        students = AddStudentInst.objects.filter(institute=inst,archieved=True)
        print(students)
        return render(request,'students/archiveStudentList.html',{'students':students})
    return HttpResponse("You are not Authenticated for This Page")



@login_required(login_url="Login")
def editStudent(request,id):
    if request.session['type']=="Institute":
        user = User.objects.get(username=request.session['user'])
        inst = Institute.objects.get(user=user)
        schools = School.objects.all()
        school_list = list(map(str,schools))
        # data = TeachingType.objects.filter(course__intitute__user=user).values_list('courseID','forclass','teachType','course')
        # processed_data = {}
        # for x in data:
        #     processed_data[x[0]] = [x[1].split(", "),x[2].split("\n")]
        student = AddStudentInst.objects.get(id=id)
        courses = Courses.objects.filter(intitute=inst)
        params = {
            'stfname':student.student.user.first_name,
            'stlname':student.student.user.last_name,
            'stemail':student.student.user.email,
            'stphone':student.student.phone,
            'address':student.student.address,
            'schoolName':student.student.schoolName,
            'courses':courses,
            'qry':student,
            "data":TeachingType.objects.filter(course__intitute=inst).values_list('forclass').distinct(),
            "school_list":school_list,
            'batch':BatchTiming.objects.filter(institute=inst),
            }
        if request.method=="POST":
            phone = request.POST.get('phone', '')
            schoolName = request.POST.get('schoolName', '')
            # ctn = request.POST.getlist('ctn_combined')
            # cn = request.POST.getlist('cn_combined')
            # ttn = request.POST.getlist('ttn_combined')
            # ttn = [x.replace("\r","") for x in ttn]
            # print('tnn--',ttn)
            # batchName = request.POST.getlist('batchN_combined')
            # feeDis = request.POST.getlist('feedis_combined')
            # installments = request.POST.getlist('noi_combined')

            ctn = request.POST.getlist('ctn')
            cn = request.POST.getlist('cn')
            ttn = request.POST.getlist('ttn')
            batchName = request.POST.getlist('batchN')
            feeDis = request.POST.getlist('feedis')
            installments = request.POST.getlist('noi')

            user = User.objects.get(username=student.student.user.username)
            studentOBJ = Student.objects.get(user=user)
            user.password = phone
            user.save()
            studentOBJ.user = user
            studentOBJ.phone = phone
            studentOBJ.address = request.POST.get("loc")
            studentOBJ.schoolName = schoolName
            studentOBJ.save()
            
            if ctn:
                student.courseName = ctn[0]
            if cn:
                student.forclass = cn[0]
            if ttn:
                student.teachType = ttn[0]
            if batchName:
                student.batch = batchName[0]
            if feeDis:
                try:
                    temp = float(feeDis[0])
                except:
                    try:
                        temp = int(feeDis[0])
                    except:
                        temp = 0
                student.feeDisc = temp
            if installments:
                student.installments=installments[0]
            student.student = studentOBJ
            student.save()

            for x in range(1,len(ttn)):
                try:
                    temp = float(feeDis[x])
                except:
                    try:
                        temp = int(feeDis[x])
                    except:
                        temp = 0

                addstudent = AddStudentInst(
                        student=studentOBJ,
                        institute=inst,
                        courseName = ctn[x] ,
                        forclass = cn[x] ,
                        teachType = ttn[x] ,
                        batch = batchName[x],
                        feeDisc = temp,
                        installments=installments[x]
                    )

            messages.success(request,"Student Updated Successfully")
            return redirect("viewStudents")
        return render(request, 'students/editStudent.html', params)
    return HttpResponse("You are not Authenticated for This Page")


@login_required(login_url="Login")
def searchUserStudent(request):
    if request.session['type']=="Institute":
        if request.method=="POST":
            print(request.POST)
            srch = request.POST.get('srh', '')
            if srch:
                match = Student.objects.filter(Q(user__username__icontains=srch) | Q(user__email__icontains=srch))
                if len(match):
                    return render(request,'students/searchUserStudent.html', {'sr':match})
                else:
                    messages.warning(request,'no result found')
        return render(request, 'students/searchUserStudent.html')
    return HttpResponse("You are not Authenticated for this view")


@login_required(login_url="Login")
def AddalreadyExistsStudent(request,id):
    if request.session['type']=="Institute":
        student = Student.objects.get(id=id)
        user = User.objects.get(username=request.session['user'])
        inst = Institute.objects.get(user=user)
        if request.method=="POST":
            # ctn = request.POST.getlist('ctn_combined')
            # cn = request.POST.getlist('cn_combined')
            # ttn = request.POST.getlist('ttn_combined')
            # ttn = [x.replace("\r","") for x in ttn]
            # batchName = request.POST.getlist('batchN_combined')
            # feeDis = request.POST.getlist('feedis_combined')
            # installments = request.POST.getlist('noi_combined')

            ctn = request.POST.getlist('ctn')
            cn = request.POST.getlist('cn')
            ttn = request.POST.getlist('ttn')
            batchName = request.POST.getlist('batchN')
            feeDis = request.POST.getlist('feedis')
            installments = request.POST.getlist('noi')
            for x in range(len(ttn)):
                try:
                    temp = float(feeDis[x])
                except:
                    try:
                        temp = int(feeDis[x])
                    except:
                        temp = 0
                addstudent = AddStudentInst(
                        student=student,
                        institute=inst,
                        courseName = ctn[x] ,
                        forclass = cn[x] ,
                        teachType = ttn[x] ,
                        batch = batchName[x],
                        feeDisc = temp,
                        installments=installments[x]
                    )
                addstudent.save()
                messages.success(request,"Student Added Successfully")
            return redirect('viewStudents')
        schools = School.objects.all()
        school_list = list(map(str,schools))
        # data = TeachingType.objects.filter(course__intitute__user=user).values_list('courseID','forclass','teachType','course')
        # processed_data = {}
        # for x in data:
        #     processed_data[x[0]] = [x[1].split(", "),x[2].split("\n")]
        return render(
            request,
            'students/addAlreadyExistsStudent.html',
            {
                "data":TeachingType.objects.filter(course__intitute=inst).values_list('forclass').distinct(),
                "student":student,
                "school_list":school_list,
                'batch':BatchTiming.objects.filter(institute=inst)
            }
        )
    return HttpResponse("You are not Authenticated for This Page")


@login_required()
def StudentCalendar(request):
    if request.session['type']=="Student":
        template = 'dashboard/student-dashboard.html'
    elif request.session['type']=="Teacher":
        template = 'dashboard/Tutor-dashboard.html'
    return render(request,'students/studentcalendar.html',{'template':template})


@login_required(login_url="Login")
def postAssignment(request):
    if request.session['type']=="Student":
        user = User.objects.get(username=request.session['user'])
        student = Student.objects.get(user=user)
        if(request.method=='POST'):
            # saving data
            classlist = ['I','II','III','IV','V','VI','VII','VIII','IX','X','XI','XII','Others','Nursery']
            forclass = request.POST.get('ctn')
            try:
                if int(forclass):
                    forclass = classlist[int(forclass)-1]
            except:
                forclass = forclass
            postAssigObj = PostAssignment(
                    student = student,
                    courseName = request.POST.get('cn'),
                    forclass = forclass,
                    description = request.POST.get('description'),
                    descriptionFile = request.FILES.get('file'),
                    requirement = request.POST.get('requirement'),
                    budget = request.POST.get('budget'),
                )
            postAssigObj.save()

        with open('cc.txt', 'r') as f:
            data = json.loads(f.read())

        return render(
            request,
            'students/postAssignment.html',
            {
                "data":data,
                'student':student
            }
        )
    return HttpResponse("You are not Authenticated for this Page")


@login_required(login_url="Login")
def postTution(request):
    if request.session['type']=="Student":
        jsonLocalData = loads(open('cc.txt','r').read())
        if(request.method=='POST'):
            print(request.POST)
            user = User.objects.get(username=request.session['user'])
            student = Student.objects.get(user=user)
            classlist = ['I','II','III','IV','V','VI','VII','VIII','IX','X','XI','XII','Others','Nursery']
            forclass = request.POST.get('className')
            try:
                if int(forclass):
                    forclass = classlist[int(forclass)-1]
            except:
                forclass = forclass
            postTutionObj = PostTution(
                    student = student,
                    subject = request.POST.get('subject'),
                    forclass = forclass,
                    teachingMode = request.POST.get('tm'),
                    genderPreference = request.POST.get('gp'),
                    whenToStart = request.POST.get('sd'),
                    description = request.POST.get('description'),
                    budget = request.POST.get('budget'),
                    budgetVal = request.POST.get('budgetvalue',0),
                    numberOfSessions =request.POST.get('monthlydigit',0)
                )
            postTutionObj.save()
        user = User.objects.get(username=request.session['user'])
        student = Student.objects.get(user=user)
        tutions = PostTution.objects.filter(student=student)
        return render(
            request,
            'students/postTution.html',
            {
                'jsonLocalData':jsonLocalData,
                'tutions':tutions
            }
        )
    return HttpResponse("You are not Authenticated for this Page")


@login_required(login_url="Login")
def delete_Assignment(request,sno):
    if request.session['type']=="Student":
        user = User.objects.get(username=request.session['user'])
        student = Student.objects.get(user=user)
        try:
            assign = PostAssignment.objects.get(sno=sno)
            if assign.student == student:
                assign.delete()
                return redirect("postAssignment")
            else:
                return HttpResponse("You are not Authenticated for this Action")
        except:
            return HttpResponse("Assignment Does Not exist")
    return HttpResponse("You are not Authenticated for this Page")



@login_required(login_url="Login")
def delete_Tution(request,sno):
    if request.session['type']=="Student":
        user = User.objects.get(username=request.session['user'])
        student = Student.objects.get(user=user)
        try:
            tution = PostTution.objects.get(sno=sno)
            if tution.student == student:
                tution.delete()
                return redirect("postTution")
            else:
                return HttpResponse("You are not Authenticated for this Action")
        except:
            return HttpResponse("Tutions Does Not exist")
    return HttpResponse("You are not Authenticated fr this Action")

def haversine(lon1, lat1, lon2, lat2):
   
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371.8 # Radius of earth in kilometers. Use 3956 for miles
    return c * r

@login_required(login_url="Login")
def enrolledStudents(request):
    prefill={}
    if request.session['type']=="Teacher":
        currentS = []
        if(request.method=='POST'):
            className = request.POST.get('className','')
            subject = request.POST.get('subject','')
            distance = request.POST.get('distance','')
            address = request.POST.get('loc')
            teachtype = request.POST.get('teachtype','')
            classlist = ['I','II','III','IV','V','VI','VII','VIII','IX','X','XI','XII','Others','Nursery']

            prefill = {
                    "address":address,
                    "distance":distance,
                    "class":className,
                    "subject":subject,
                    "type":teachtype
            }

            try:
                if int(className):
                    className = classlist[int(className)-1]
            except:
                className = className

            if distance=="":
                distance=0
            
            distance = float(distance)

            geolocator = Nominatim(user_agent="inst")

            city = geolocator.geocode(address, timeout=None)
            if city:
                cityLat = city.latitude
                cityLng = city.longitude

            else:
                cityLat = float(request.POST.get('cityLat',''))
                cityLng = float(request.POST.get('cityLng',''))
            
            tutions = PostTution.objects.all()

            if(subject):
                tutions = tutions.filter(Q(subject=subject))
            if(className):
                tutions = tutions.filter(Q(forclass=className))
            if(teachtype):
                tutions = tutions.filter(Q(teachingMode=teachtype))

            for tut in tutions:
                std = tut.student
                location = geolocator.geocode(std.address, timeout=None)
                if location:
                    Lat = location.latitude
                    Lng = location.longitude
                    if haversine(Lng,Lat,cityLng,cityLat) <=distance:
                        if tut not in currentS:
                            currentS.append(tut)
        jsonLocalData = loads(open('cc.txt','r').read())
        return render(request, "students/enrolledStudents.html",{'allData':currentS,'jsonLocalData':jsonLocalData,'prefill':prefill})
    return HttpResponse("You are not Authenticated for this Page")



@login_required(login_url="Login")
def ChatStudent(request):
	user = User.objects.get(username=request.session['user'])
	student = Student.objects.get(user=user)
	context = {
	'student':student
	}
	return render(request,'teacher/ChatTutor.html',context)

