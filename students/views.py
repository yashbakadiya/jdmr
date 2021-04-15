from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.decorators import login_required
from accounts.models import Institute,Teacher,Student
from django.contrib import messages
from courses.models import TeachingType,Courses
from batches.models import BatchTiming
from .models import AddStudentInst,School,PostTution,PostAssignment
from datetime import datetime,timedelta
from django.contrib.auth.models import User
from json import dumps
from django.core.serializers.json import DjangoJSONEncoder
from django.forms.models import model_to_dict
import json
from django.db.models import Q
from json import dumps,loads 
import os
from datetime import datetime
from math import radians, sin, cos, asin, sqrt
from geopy.geocoders import Nominatim
from get_notice import notice
from batches.models import Notice
from teacher.models import MakeAppointment
from dateutil import parser,rrule
import pytz

# Create your views here.
allTimezones = pytz.all_timezones

@login_required(login_url="Login")
def stuShowAllNotice(request):
    if request.session['type'] == "Student":
        user = User.objects.get(username=request.session['user'])
        student = Student.objects.get(user=user)
        appointments = MakeAppointment.objects.filter(created_by=True, student=student, accepted=False)
        notices = notice(request)
        return render(request, "batches/stu_showAllNotice.html", context={"notices":notices, 'appointments':appointments})
    return HttpResponse("You are not Authenticated for This Page")


@login_required(login_url="Login")
def stuShowNotice(request, id):
    notice = Notice.objects.get(id=id)
    return render(request, "batches/stu_showNotice.html", context={"notice":notice})


@login_required(login_url="Login")
def rejectAppointment(request, pk):
    if request.session['type'] == "Student":
        appointment = MakeAppointment.objects.get(pk=pk)
        appointment.delete()
        return redirect('stuShowAllNotice')
    return HttpResponse("You are not Authenticated for This Page")


@login_required(login_url="Login")
def acceptAppointment(request, pk):
    if request.session['type'] == "Student":
        appointment = MakeAppointment.objects.get(pk=pk)
        appointment.accepted = True
        appointment.save()
        return redirect('stuShowAllNotice')
    return HttpResponse("You are not Authenticated for This Page")


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
                    temp = 0
                try:
                    insttemp = float(installments[x])
                except:
                    insttemp = 0
                
                addstudent = AddStudentInst.objects.get_or_create(student=student,institute=inst,courseName = ctn[x],forclass = cn[x],teachType = ttn[x])[0]
                addstudent.batch = batchName[x]
                addstudent.feeDisc = temp
                addstudent.installments=insttemp
                addstudent.save()
            messages.success(request,"Student Added Successfully")
            return redirect('viewStudents')

        schools = School.objects.all()
        school_list = list(map(str,schools))
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
        students = set([x.student for x in AddStudentInst.objects.filter(institute=inst,archieved=False)])
        courses = []
        forclass = []
        teachType = []

        for student in students:
            courses.append(','.join([x[0] for x in AddStudentInst.objects.filter(institute=inst,archieved=False,student=student).values_list('courseName').distinct()]))
            forclass.append(','.join([x[0] for x in AddStudentInst.objects.filter(institute=inst,archieved=False,student=student).values_list('forclass').distinct()]))
            teachType.append(','.join([x[0] for x in AddStudentInst.objects.filter(institute=inst,archieved=False,student=student).values_list('teachType').distinct()]))
        
        students = zip(students,courses,forclass,teachType)
        params = {'students':students,"size":len(courses)}

        if request.method == "POST":
            check = request.POST.getlist('check')
            for x in check:
                for arStudent in AddStudentInst.objects.filter(student=Student.objects.get(id = int(x))):
                    arStudent.archieved = True
                    arStudent.save()
            messages.success(request,"Student Added To Archieve Successfully")
            return redirect('viewStudents')
        return render(request, 'students/viewStudents.html', params)
    return HttpResponse("You are not Authenticated for This Page")

@login_required(login_url="Login")
def deleteStudent(request,id):
    if request.session['type'] == "Institute":
        delStu = AddStudentInst.objects.get(student=Student.objects.filter(id = id)).delete()
        messages.warning(request,"Student Deleted Successfully")
        return redirect("viewStudents")
    return HttpResponse("You are not Authenticated for This Page")

def archiveStudentList(request):
    if request.session['type'] == "Institute":
        user = User.objects.get(username=request.session["user"])
        inst = Institute.objects.get(user=user)
        students = set([x.student for x in AddStudentInst.objects.filter(institute=inst,archieved=True)])
        courses = []
        forclass = []
        teachType = []

        for student in students:
            courses.append(','.join([x[0] for x in AddStudentInst.objects.filter(institute=inst,archieved=True,student=student).values_list('courseName').distinct()]))
            forclass.append(','.join([x[0] for x in AddStudentInst.objects.filter(institute=inst,archieved=True,student=student).values_list('forclass').distinct()]))
            teachType.append(','.join([x[0] for x in AddStudentInst.objects.filter(institute=inst,archieved=True,student=student).values_list('teachType').distinct()]))
        
        students = zip(students,courses,forclass,teachType)
        params = {'students':students,"size":len(courses)}

        if request.method == "POST":
            check = request.POST.getlist('check')
            for x in check:
                for arStudent in AddStudentInst.objects.filter(student=Student.objects.get(id = int(x))):
                    arStudent.archieved = False
                    arStudent.save()
            messages.success(request,"Student Added To Archieve Successfully")
            return redirect('viewStudents')
        return render(request,'students/archiveStudentList.html',params)
    return HttpResponse("You are not Authenticated for This Page")

@login_required(login_url="Login")
def editStudent(request,id):
    if request.session['type']=="Institute":
        user = User.objects.get(username=request.session['user'])
        inst = Institute.objects.get(user=user)
        schools = School.objects.all()
        school_list = list(map(str,schools))
        student = Student.objects.get(id=id)
        editStudentObj = AddStudentInst.objects.filter(student=student)
        if request.method=="POST":
            phone = request.POST.get('phone', '')
            schoolName = request.POST.get('schoolName', '')
            ctn = request.POST.getlist('ctn')
            cn = request.POST.getlist('cn')
            ttn = request.POST.getlist('ttn')
            batchName = request.POST.getlist('batchN')
            feeDis = request.POST.getlist('feedis')
            installments = request.POST.getlist('noi')
            
            user = User.objects.get(username=student.user.username)
            student.address = request.POST.get("loc")
            student.schoolName = schoolName
            student.save()

            if ttn:
                editStudentObj.delete()

                for x in range(len(ttn)):
                    try:
                        temp = float(feeDis[x])
                    except:
                        temp = 0
                    try:
                        insttemp = float(installments[x])
                    except:
                        insttemp = 0

                    addstudent = AddStudentInst.objects.get_or_create(student=student,institute=inst,courseName = ctn[x],forclass = cn[x],teachType = ttn[x])[0]
                    addstudent.batch = batchName[x]
                    addstudent.feeDisc = temp
                    addstudent.installments=insttemp
                    addstudent.save()

            messages.success(request,"Student Updated Successfully")
            return redirect("viewStudents")
        return render(request, 'students/editStudent.html', {
            "studentBaseData":student,
            "data":TeachingType.objects.filter(course__intitute=inst).values_list('forclass').distinct(),
            "school_list":school_list,
            "editStudent":editStudentObj
            })
    return HttpResponse("You are not Authenticated for This Page")

@login_required(login_url="Login")
def searchUserStudent(request):
    if request.session['type']=="Institute":
        if request.method=="POST":
            print(request.POST)
            srch = request.POST.get('srh', '')
            if srch:
                match = Student.objects.filter(Q(phone=srch) | Q(user__email=srch) | Q(user__username=srch))
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

        if AddStudentInst.objects.filter(institute=inst,student=student):
            messages.warning(request,"Student Already Added")
            return redirect("viewStudents")

        if request.method=="POST":
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
                    temp = 0
                try:
                    insttemp = float(installments[x])
                except:
                    insttemp = 0
                
                addstudent = AddStudentInst.objects.get_or_create(student=student,institute=inst,courseName = ctn[x],forclass = cn[x],teachType = ttn[x])[0]
                addstudent.batch = batchName[x]
                addstudent.feeDisc = temp
                addstudent.installments=insttemp
                addstudent.save()
            messages.success(request,"Student Added Successfully")
            return redirect('viewStudents')

        schools = School.objects.all()
        school_list = list(map(str,schools))
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
    makepoint = MakeAppointment.objects.all()
    return render(request,'students/studentcalendar.html',{'template':template,'makepoint':makepoint})

@login_required(login_url="Login")
def postAssignment(request):
    if request.session['type']=="Student":
        user = User.objects.get(username=request.session['user'])
        student = Student.objects.get(user=user)
        if request.method=='POST':
            deadline = request.POST.get('deadline')
            forclass = request.POST.get('ctn')

            postAssigObj = PostAssignment(
                    student = student,
                    courseName = request.POST.get('cn'),
                    forclass = forclass,
                    description = request.POST.get('description'),
                    descriptionFile = request.FILES.get('file'),
                    budget = request.POST.get('budget'),
                )

            if deadline:
                postAssigObj.deadline = datetime.strptime(deadline,'%Y-%m-%d')
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
def extendDeadline(request,id):
    if request.session['type']=="Student":
        if request.method=='POST':
            extend = request.POST.get('extend')
            if extend:
                postAssigObj = postAssignment.objects.get(id=id)
                postAssigObj.deadline = datetime.strptime(extend,"%Y-%m-%d")
                postAssigObj.save()
        return redirect('postAssignment')
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

def checkClashes(person,utcDateTime,duration,recc,pattern,repeat,days,utcEndingdate,daysDump):
	# return 1 for clash and 0 for no clash
	appointments = person.MakeAppointment.all()
	for appointment in appointments:
		for x in json.loads(appointment.daysDump):
			print(x,appointment.duration)
			dts = parser.parse(x)
			for y in daysDump:
				print(y,duration)
				if(dts<=y<=dts+appointment.duration or dts<=y+duration<=dts+appointment.duration):
					return 1
	return 0

def createReccurance(utcDateTime,duration,recc,pattern,repeat,days,utcEndingdate):
	allDays = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
	if(recc):
		if(pattern=='D'):
			days = allDays
			repeat = 1
		dayConv = {'Mon':rrule.MO,'Tue':rrule.TU,'Wed':rrule.WE,'Thu':rrule.TH,'Fri':rrule.FR,'Sat':rrule.SA,'Sun':rrule.SU}
		daysDump = [utcDateTime]+list(rrule.rrule(rrule.WEEKLY, interval=repeat,wkst=rrule.MO, byweekday=[dayConv[x] for x in days],until=utcEndingdate,dtstart=utcDateTime))
	else:
		daysDump = [utcDateTime]
	return daysDump


@login_required(login_url="Login")
def stuMakeAppointment(request,id):
    if request.session['type']=="Student":
        user = User.objects.get(username=request.session['user'])
        student = Student.objects.get(user=user)
        tutor = Teacher.objects.get(id=id)
        if request.method=='GET':
            return render(request,'students/by_student_appointment.html')
        if request.method=='POST':
            # errors list
            errors = []
            # input date
            date = request.POST.get('date')
            try:
                # date conversion
                date = datetime.strptime(date,'%Y-%m-%d')
            except Exception as e:
                errors.append(f"Date is in wrong format > {date}")
            #input time
            time = request.POST.get('time')
            try:
                #time conversion
                time = datetime.strptime(time,'%H:%M')
            except Exception as e:
                errors.append(f"Date is in wrong format > {date}")
            try:
                #joining date and time
                dateTimeObj = datetime(
                                year=date.year,
                                month=date.month,
                                day=date.day,
                                hour=time.hour,
                                minute=time.minute,
                                second=time.second
                            )
            except Exception as e:
                errors.append("Date or Time is wrong")

            #input duration hour
            durationHour = request.POST.get('durationHour')
            try:
                #convert to int
                durationHour = int(durationHour)
            except Exception as e:
                errors.append("Duration Hour should be an integer.")

            #input duration minute
            durationMinute = request.POST.get('durationMinute')
            try:
                #convert to int
                durationMinute = int(durationMinute)
            except Exception as e:
                errors.append("Duration Minute should be an integer.")

            #create single duration timedelta object
            try:
                duration = timedelta(hours=durationHour,minutes=durationMinute)
            except Exception as e:
                errors.append("Duration minute or hour is incorrect.")

            #input timezone
            timezone = request.POST.get('timezone')
            if(timezone not in allTimezones):
                errors.append("Wrong timezone")

            #creating old timezone object
            try:
                old_timezone = pytz.timezone(timezone)
            except:
                errors.append("Wrong timezone conversion")

            #new uc time zone object
            new_timezone = pytz.timezone("UTC")

            #conveting old timezone data to utc
            try:
                utcDateTime = old_timezone.localize(dateTimeObj).astimezone(new_timezone)
            except:
                errors.append('Timezone conversion error!')

            #reccurance input
            recc = request.POST.get('recc')
            if(recc=='on'):
                recc=True
            else:
                recc=False

            #recurance daily(D) or weekly(W)
            pattern = request.POST.get('recPattern')

            #reccurance on every (_)
            repeat = request.POST.get('repeat',1)
            if(repeat):
                try:
                    repeat = int(repeat)
                except Exception as e:
                    errors.append('Repeat should be an integer.')

            #days list
            days = request.POST.getlist('days')

            #no(infinite)/ end(date)/ number(of meetings)

            #ending date and conversion to utc
            endingdate = request.POST.get('endingDate')
            if(endingdate):
                try:
                    endingdate = datetime.strptime(endingdate,'%Y-%m-%d')
                    utcEndingdate = old_timezone.localize(endingdate).astimezone(new_timezone)
                except Exception as e:
                    errors.append(f"Date is in wrong format > {date}")
            else:
                endingdate = dateTimeObj + duration
                try:
                    utcEndingdate = old_timezone.localize(endingdate).astimezone(new_timezone)
                except Exception as e:
                    errors.append(f"Date is in wrong format > {date}")

            daysDump = createReccurance(utcDateTime,duration,recc,pattern,repeat,days,utcEndingdate)
            #checking clashes for student
            try:
                if(checkClashes(student,utcDateTime,duration,recc,pattern,repeat,days,utcEndingdate,daysDump)):
                    errors.append("This appontment cannot be created as you already have an appointment during this duration.")
            except Exception as e:
                errors.append("There was an error while creating this appointment for you.")

            #checking clashes for tutor
            try:
                if(checkClashes(tutor,utcDateTime,duration,recc,pattern,repeat,days,utcEndingdate,daysDump)):
                    errors.append("This appontment cannot be created as this tutor already have an appointment during this duration.")
            except Exception as e:
                errors.append("There was an error whicle creating this appointment for the student.")

            #if there are any error
            if(errors):
                return JsonResponse({
                    'status':0,
                    'errors':errors
                    })

            #if no error
            else:
                appointmentObj = MakeAppointment(
                        dateTime    = dateTimeObj,
                        duration    = duration,
                        timezone    = timezone,
                        recc        = recc,
                        pattern     = pattern,
                        repeat      = repeat,
                        days        = days,
                        endingDate  = endingdate,
                        tutor       = tutor,
                        student     = student,
                        utcDateTime = utcDateTime,
                        utcEndingDate=utcEndingdate,
                        daysDump     = json.dumps(daysDump, cls=DjangoJSONEncoder)
                    )
                try:
                    appointmentObj.save()
                    return redirect('dashboard')
                except:
                    errors.append("something went wrong")
                    return render(request,'students/by_student_appointment.html')
        return HttpResponse("<br><h1 align='center'>¯\\_(ツ)_/¯ oops something wrong</h1>")
    return HttpResponse("You are not Authenticated for this page")







@login_required(login_url="Login")
def enrolledStudents(request):
    if request.session['type']=="Teacher":
        user = User.objects.get(username=request.session['user'])
        tutor = Teacher.objects.get(user=user)
        currentS = []
        prefill={}

        data={}
        class_list = tutor.forclass.split(',')
        unique_class = list(set(class_list))
        course_list = tutor.course.split(',')

        for i in range(len(class_list)):
            currentS.extend(PostTution.objects.filter(forclass = class_list[i], subject = course_list[i]))

        for i in  range(len(unique_class)):
            courses_of_class =[]
            for j in range(len(class_list)):
                if class_list[j] == unique_class[i]:
                    courses_of_class.append(course_list[j])
            data[unique_class[i]] = courses_of_class

        if request.method=='POST':
            className = request.POST.get('className','')
            subject = request.POST.get('subject','')
            distance = request.POST.get('distance','')
            address = request.POST.get('loc','')
            teachtype = request.POST.get('teachtype','')

            prefill = {
                    "address":address,
                    "distance":distance,
                    "class":className,
                    "course":subject,
                    "type":teachtype
            }

            tutions=[]

            if address:
                if distance:
                    distance = float(distance)
                
                else:
                    distance = 0

                geolocator = Nominatim(user_agent="inst")

                city = geolocator.geocode(address, timeout=None)
                if city:
                    cityLat = city.latitude
                    cityLng = city.longitude

                else:
                    cityLat = float(request.POST.get('cityLat',''))
                    cityLng = float(request.POST.get('cityLng',''))


                for tut in currentS:
                    std = tut.student
                    location = geolocator.geocode(std.address, timeout=None)
                    if location:
                        Lat = location.latitude
                        Lng = location.longitude
                        if haversine(Lng,Lat,cityLng,cityLat) <=distance:
                            if tut not in currentS:
                                tutions.append(tut)
                currentS = tutions
            currentS = [x.pk for x in currentS]
            currentS = PostTution.objects.filter(pk__in=currentS)
            print(currentS,address)

            if subject:
                currentS = currentS.filter(subject=subject)
                print(currentS,subject)
            if className:
                currentS = currentS.filter(forclass=className)
                print(currentS,className)
            if teachtype:
                currentS = currentS.filter(teachingMode=teachtype)
                print(currentS,teachtype)

        
        context = {
            'classes':sorted(unique_class,key=lambda a:int(a)),
            'data':data,
            'allData':currentS,
            'prefill':prefill,
            'types':['Online Tutor','Group','Home Tutor']
            }
            
        return render(request, "students/enrolledStudents.html",context)
    return HttpResponse("You are not Authenticated for this Page")



@login_required(login_url="Login")
def ChatStudent(request):
	user = User.objects.get(username=request.session['user'])
	student = Student.objects.get(user=user)
	context = {
	'student':student
	}
	return render(request,'teacher/ChatTutor.html',context)

