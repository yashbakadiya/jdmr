from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.decorators import login_required
from accounts.models import Institute,Teacher,Student
from django.contrib import messages
from courses.models import TeachingType,Courses
from json import dumps,loads
from .models import enrollTutors,TutorRatings,MakeAppointment
from django.contrib.auth.models import User
from django.db.models import Q
from students.models import *
from dateutil import parser,rrule
import pytz
from datetime import datetime,timedelta
import datetime as dt
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
import json
from geopy.geocoders import Nominatim 
from math import radians, sin, cos, asin, sqrt
from get_notice import notice
from batches.models import Notice
# Create your views here.

allTimezones = pytz.all_timezones


@login_required(login_url="Login")
def teaShowAllNotice(request):
    if request.session['type'] == "Teacher":
        user = User.objects.get(username=request.session['user'])
        teacher = Teacher.objects.get(user=user)
        appointments = MakeAppointment.objects.filter(created_by=False, tutor=teacher , accepted=False)
        notices = notice(request)
        return render(request, "batches/tea_showAllNotice.html", context={"notices":notices, 'appointments':appointments})
    return HttpResponse("You are not Authenticated for This Page")


@login_required(login_url="Login")
def teaShowNotice(request, id):
    notice = Notice.objects.get(id=id)
    return render(request, "batches/tea_showNotice.html", context={"notice":notice})


@login_required(login_url="Login")
def rejectAppointment(request, pk):
    if request.session['type'] == "Teacher":
        appointment = MakeAppointment.objects.get(pk=pk)
        appointment.delete()
        return redirect('teaShowAllNotice')
    return HttpResponse("You are not Authenticated for This Page")


@login_required(login_url="Login")
def acceptAppointment(request, pk):
    if request.session['type'] == "Teacher":
        appointment = MakeAppointment.objects.get(pk=pk)
        appointment.accepted = True
        appointment.save()
        return redirect('teaShowAllNotice')
    return HttpResponse("You are not Authenticated for This Page")


@login_required(login_url="Login")
def addTutors(request):
    errors = []
    if request.session['type'] == "Institute":
        user = User.objects.get(username=request.session['user'])
        inst = Institute.objects.get(user=user)
        cours = Courses.objects.all()
        teach=TeachingType.objects.all()

        if request.method == "POST":
            print(request.POST)
            firstName = request.POST.get('firstName', '')
            lastName = request.POST.get('lastName', '')
            email = request.POST.get('email', '')
            phone = request.POST.get('phone', '')
            password = phone
            username = email
            location = request.POST.get('loc', '')
            if firstName.isalpha() == False | lastName.isalpha() == False:
                messages.warning(request,"Name must be alphabetical")
            if len(phone) != 10:
                messages.warning(request,"Phone Number must be 10 digits")
            if phone.isdigit() == False:
                messages.warning(request,"Phone Number must be numeric")
            if User.objects.filter(email=email).exists():
                messages.warning(request,"Email Already Exists")
            if Teacher.objects.filter(phone=phone).exists():
                messages.warning(request,"Phone No is Already Registered")
            if(errors):
                return render(request, 'tutor/signupTutor.html',{"errors":errors})
            else:
                user2=User(username=username,email=email,password=password,first_name=firstName,last_name=lastName)
                user2.save()
                teacher = Teacher(user=user2,address=location,phone=phone)
                teacher.save()
                # ctn = request.POST.getlist('ctn_combined')
                # cn = request.POST.getlist('cn_combined')
                # ttn = request.POST.getlist('ttn_combined')
                # ttn = [x.replace("\r","") for x in ttn]

                ctn = request.POST.getlist('ctn')
                cn = request.POST.getlist('cn')
                ttn = request.POST.getlist('ttn')

                availability = request.POST.get('availability')
                if(availability=='weekly'):
                    availability='weekly'
                elif(availability=='weekend'):
                    availability='weekend'
                elif(availability=='both'):
                    availability='weekly,weekend'
                else:
                    availability="not available"
                for x in range(len(ttn)):
                    addTeacher = enrollTutors(forclass=cn[x],teachType=ttn[x],courseName=ctn[x],institute=inst,teacher=teacher,availability=availability)
                    addTeacher.save()
                messages.success(request,"Teacher Added Successfully")
                return redirect("viewTutors")

        # data = TeachingType.objects.values_list('courseID','forclass','teachType','course')
        # processed_data = {}
        # for x in data:
        #     processed_data[x[0]] = [x[1].split(", "),x[2].split("\n")]
        return render(request,'teacher/addTutors.html',
            {
                "data":TeachingType.objects.filter(course__intitute=inst).values_list('forclass').distinct(),"cours":cours,"teach":teach,
            }
        )
    return HttpResponse("You Are Not Authenticated for this view")


@login_required(login_url="Login")
def viewTutors(request):
    if request.session['type'] == "Institute":
        user = User.objects.get(username=request.session['user'])
        inst = Institute.objects.get(user=user)
        tutors = enrollTutors.objects.filter(institute=inst,archieved=False)
        courses = Courses.objects.filter(intitute=inst,archieved=False)
        courselist = []
        for course in courses:
            for tutor in tutors:
                if tutor.courseName:
                    if tutor.courseName==course.courseName:
                        courselist.append(course.courseName)
        tutors = zip(tutors,courselist)
        params = {'tutors':tutors}
        if request.method=="POST":
            check = request.POST.getlist('check')
            for x in check:
                arTutor = enrollTutors.objects.get(id = int(x))
                arTutor.archieved = True
                arTutor.save()
            messages.success(request,"Teacher Added To Archieve Successfully")
            return redirect('viewTutors')
        return render(request, 'teacher/viewTutors.html', params)
    return HttpResponse("You Are Not Authenticated for this view")



@login_required(login_url="Login")
def deleteTutor(request,id):
    if request.session['type'] == "Institute":
        delobj = enrollTutors.objects.get(id=id)
        delobj.delete()
        messages.warning(request,"Teacher Deleted Successfully")
        return redirect("viewTutors")
    return HttpResponse("You Are Not Authenticated for this view")



@login_required(login_url="Login")
def editTutor(request,id):
    if request.session['type'] == "Institute":
        user = User.objects.get(username=request.session['user'])
        inst = Institute.objects.get(user=user)
        editTutorObj = enrollTutors.objects.get(id = id)
        teacher = Teacher.objects.get(user__username=editTutorObj.teacher.user.username)
        # data = TeachingType.objects.values_list('courseID','forclass','teachType','course')
        # processed_data = {}
        # for x in data:
        #     processed_data[x[0]] = [x[1].split(", "),x[2].split("\n")]
        if request.method == "POST":
            # ctn = request.POST.get('ctn_combined')
            # cn = request.POST.get('cn_combined')
            # ttn = request.POST.get('ttn_combined')
            ctn = request.POST.getlist('ctn')
            cn = request.POST.getlist('cn')
            ttn = request.POST.getlist('ttn')
            availability = request.POST.get('availability')
            if(availability=='weekly'):
                availability='weekly'
            elif(availability=='weekend'):
                availability='weekend'
            elif(availability=='both'):
                availability='weekly,weekend'
            else:
                availability="not available"
            NewUsername = request.POST.get("NewUsername")
            NewEmail = request.POST.get("NewEmail")
            NewPhone = request.POST.get("NewPhone")
            teacher.name = NewUsername
            teacher.email = NewEmail
            teacher.password = NewPhone
            teacher.phone = NewPhone
            teacher.save()
            user = User.objects.get(username=editTutorObj.teacher.user.username)
            user.username = NewUsername
            user.password = NewPhone
            user.email = NewEmail
            user.save()
            inst = Institute.objects.get(user=User.objects.get(username=request.session['user']))

            if ctn:    
                editTutorObj.courseName = ctn[0]
            if cn:
                editTutorObj.forclass = cn[0]
            if ttn:
                editTutorObj.teachType = ttn[0]
            editTutorObj.teacher = teacher
            editTutorObj.availability = availability
            editTutorObj.save()

            for x in range(1,len(ttn)):
                addTeacher = enrollTutors(forclass=cn[x],teachType=ttn[x],courseName=ctn[x],institute=inst,teacher=teacher,availability=availability)
                addTeacher.save()
                
            messages.success(request,"Teacher Updated Successfully")
            return redirect("viewTutors")
        return render(request,"teacher/editTutorMini.html",{
                "data":TeachingType.objects.filter(course__intitute=inst).values_list('forclass').distinct(),
                "tutorBaseData":teacher,
                "editTutor":editTutorObj
            })
    return HttpResponse("You Are Not Authenticated for this view")



@login_required(login_url="Login")
def archiveTutorList(request):
    if request.session['type'] == "Institute":
        user = User.objects.get(username=request.session['user'])
        inst = Institute.objects.get(user=user)
        if request.method == "POST":
            check = request.POST.getlist('check')
            for x in check:
                arTutor = enrollTutors.objects.get(id = int(x))
                arTutor.archieved = False
                arTutor.save()
            messages.success(request,"Teacher Removed From Archieve Successfully")
            return redirect('archiveTutorList')
        tutor = enrollTutors.objects.filter(institute=inst,archieved=True)
        params = {'tutor':tutor}
        return render(request, 'teacher/archiveTutorList.html', params)
    return HttpResponse("You Are Not Authenticated for this view")



@login_required(login_url="Login")
def searchUserTutor(request):
    if request.session['type'] == "Institute":
        if request.method=="POST":
            srch = request.POST.get('srh', '')
            if srch:
                teacher = Teacher.objects.filter(Q(phone=srch) | Q(user__email=srch))
                if teacher:
                    return render(request,'teacher/searchUserTutor.html', {'sr':teacher})
                else:
                    messages.warning(request,'no result found')
                    return redirect("addTutors")
            else:
                messages.warning(request,'no result found')
                return redirect("addTutors")
    return HttpResponse("You Are Not Authenticated for this page")



@login_required(login_url="Login")
def AddalreadyExistsTutor(request,id):
    if request.session['type']=="Institute":
        teacher = Teacher.objects.get(id=id)
        user = User.objects.get(username=request.session['user'])
        inst = Institute.objects.get(user=user)
        if request.method=="POST":
            # ctn = request.POST.getlist('ctn_combined')
            # cn = request.POST.getlist('cn_combined')
            # ttn = request.POST.getlist('ttn_combined')
            # ttn = [x.replace("\r","") for x in ttn]
            ctn = request.POST.getlist('ctn')
            cn = request.POST.getlist('cn')
            ttn = request.POST.getlist('ttn')
            availability = request.POST.get('availability')
            if(availability=='weekly'):
                availability='weekly'
            elif(availability=='weekend'):
                availability='weekend'
            elif(availability=='both'):
                availability='weekly,weekend'
            else:
                availability="not available"
            for x in range(len(ttn)):
                addTeacher = enrollTutors(forclass=cn[x],teachType=ttn[x],courseName=ctn[x],institute=inst,teacher=teacher,availability=availability)
                addTeacher.save()
            messages.success(request,"Teacher Added Successfully")
            return redirect("viewTutors")

        # data = TeachingType.objects.values_list('courseID','forclass','teachType','course')
        # processed_data = {}
        # for x in data:
        #     processed_data[x[0]] = [x[1].split(", "),x[2].split("\n")]
        return render(
            request,
            'teacher/addTutorExist.html',
            {
                "data":TeachingType.objects.filter(course__intitute=inst).values_list('forclass').distinct(),
                'teacher':teacher
            }
        )
    return HttpResponse("You Are Not Authenticated for this view")


def enrolledTutorsObjectToDict(obj):
    data = {
        'id':obj.id,
        'username':obj.user.username,
        'firstName':obj.user.first_name,
        'lastName':obj.user.last_name,
        'email':obj.user.email,
        'address':obj.address,
        'phone':obj.phone,
        'availability':obj.availability,
        'qualification':obj.qualification,
        'experience':obj.experiance,
        'gender':obj.gender,
        'fees':obj.fees,
        'forclass':obj.forclass
    }
    if obj.photo:
        data['photo']=obj.photo.url
    
    courseID = obj.course.replace(";",'')
    courseID = list(set(courseID))
    courses = []
    for i in courseID:
        try:
            course = Courses.objects.get(id = i)
            courses.append(course.courseName)
        except:
            pass
    data['courseName']=courses
    return data

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
def enrolledTutors(request):
    jsonLocalData = loads(open('cc.txt','r').read())
    
    prefill = {}
    if request.method == "POST":
        className = request.POST.get('className','')
        loc = request.POST.get('loc','')
        distance = request.POST.get('distance','')
        subject = request.POST.get('subject','')
        experience = request.POST.get('experience','')
        prefill = {
            "address":loc,
            "class":className,
            "subject":subject,
            "experience":experience,
            "distance":distance
        }
        classlist = ['I','II','III','IV','V','VI','VII','VIII','IX','X','XI','XII','Others','Nursery']
        try:
            if int(className):
                className = classlist[int(className)-1]
        except:
            className = className
        if experience=="":
            experience=1

        if distance=="":
            distance=0
        
        distance = float(distance)

        geolocator = Nominatim(user_agent="geoapiExercises")
        city = geolocator.geocode(loc, timeout = None)
        if city:
            cityLat = city.latitude
            cityLng = city.longitude

        else:
            cityLat = request.POST.get('cityLat','')
            cityLng = request.POST.get('cityLng','')

        if subject:
            searchQuery = Teacher.objects.filter(Q(course__icontains=subject))

        if className:
            searchQuery = Teacher.objects.filter(Q(forclass__icontains=className))            

        if experience:
            searchQuery = Teacher.objects.filter(Q(experiance__gte=int(experience)))

        allData = []
        
        for x in searchQuery:
            location = geolocator.geocode(x.address, timeout=None)
            if location:
                if haversine(location.longitude,location.latitude,cityLng,cityLat) <= distance:
                    allData.append(x)

        jsonData = []
        for x in allData:
            jsonData.append(enrolledTutorsObjectToDict(x))
            
        return render(request, "teacher/enrolledTutors.html",{'allData':allData,'jsonData':jsonData,'jsonLocalData':jsonLocalData,"prefill":prefill})
    allData = []
    jsonData = []
    for x in allData:
        jsonData.append(enrolledTutorsObjectToDict(x))
    return render(request,'teacher/enrolledTutors.html',{'allData':allData,'jsonData':jsonData,'jsonLocalData':jsonLocalData,"prefill":prefill})
	

@login_required(login_url="Login")
def ReviewTutors(request,tutor_id):
    if request.session['type']=="Student":
        user = User.objects.get(username=request.session['user'])
        student = Student.objects.get(user=user)
        tutor = Teacher.objects.get(id=tutor_id)
        reviews = TutorRatings.objects.filter(Tutor=tutor)
        currentStudent = True
        if TutorRatings.objects.filter(Q(Student=student) and Q(Tutor=tutor)).exists():
            currentStudent = False
        count = reviews.count()
        sumRating = 0
        for i in reviews:
            add = i.Rating
            sumRating+=add
        try:
            avgRating = sumRating/count
        except:
            avgRating = 0
        context = {
        'i':tutor,
        'reviews':reviews,
        'avgRating':range(int(avgRating)),
        'currentStudent':currentStudent
        }
        if request.method == "POST" and not(TutorRatings.objects.filter(Q(Student=student) and Q(Tutor=tutor)).exists()):
            rating =request.POST.get("rating","")
            comment = request.POST.get("comment","")
            print(rating,comment)
            data = TutorRatings(
                Tutor = tutor,
                Student=student,
                Review=comment,
                Rating = rating)
            data.save()
            return redirect('reviewtutor',tutor_id)
        return render(request,'teacher/Reviewstutor.html',context)
    return HttpResponse("You are not Authenticated for this page")    

@login_required(login_url="Login")
def ChatTutor(request,tutor_id):
	try:
		tutor = Teacher.objects.get(id=tutor_id)
		user = User.objects.get(username=request.session['user'])
		student = Student.objects.get(user=user)
	except:
		return redirect('enrolledTutors')
	context = {
	'tutor':tutor,
	'student':student
	}
	return render(request,'teacher/ChatTutor.html',context)


@login_required(login_url="Login")
def ChatStudent(request):
	user = User.objects.get(username=request.session['user'])
	tutor = Teacher.objects.get(user=user)
	context = {
	'tutor':tutor}
	return render(request,'students/chatStudent.html',context)



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
def teaMakeAppointment(request,id):
    if request.session['type']=="Teacher":
        user = User.objects.get(username=request.session['user'])
        tutor = Teacher.objects.get(user=user)
        student = Student.objects.get(id=id)
        if request.method=='GET':
            return render(request,'teacher/by_teacher_appointment.html')
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
                if(checkClashes(tutor,utcDateTime,duration,recc,pattern,repeat,days,utcEndingdate,daysDump)):
                    errors.append("This appontment cannot be created as you already have an appointment during this duration.")
            except Exception as e:
                errors.append("There was an error while creating this appointment for you.")

            #checking clashes for tutor
            try:
                if(checkClashes(student,utcDateTime,duration,recc,pattern,repeat,days,utcEndingdate,daysDump)):
                    errors.append("This appontment cannot be created as this student already have an appointment during this duration.")
            except Exception as e:
                errors.append("There was an error whicle creating this appointment for the tutor.")

            print(utcEndingdate)
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
                        daysDump     = json.dumps(daysDump, cls=DjangoJSONEncoder),
                        created_by  = 1
                    )
                try:
                    appointmentObj.save()
                    return redirect('dashboard')
                except:
                    errors.append("something went wrong")
                    return render(request,'teacher/by_teacher_appointment.html')
        return HttpResponse("<br><h1 align='center'>¯\\_(ツ)_/¯ oops something wrong</h1>")
    return HttpResponse("You are not Authenticated for this page")






@login_required(login_url="Login")
def viewAssignmentTutor(request):
    currentS = {}
    prefill={}
    if request.method == "POST":
        className = request.POST.get('className',"")
        courseName = request.POST.get('subject',"")
        address = request.POST.get('loc')
        budgetVal = request.POST.get('budget')

        prefill = {
            "address":address,
            "budget":budgetVal,
            "class":className,
            "subject":courseName,
        }

        classlist = ['I','II','III','IV','V','VI','VII','VIII','IX','X','XI','XII','Others','Nursery']
        try:
            if int(className):
                className = classlist[int(className)-1]
        except:
            className = className

        if budgetVal:
            budgetVal = float(budgetVal)
        else:
            budgetVal = 100.0
        currentS = PostAssignment.objects.filter(Q(student__address__icontains=address) or Q(budget__gte=float(budgetVal)))
        if className:
            currentS = currentS.filter(Q(forclass__icontains=className))
        if courseName:
            currentS = currentS.filter(Q(courseName__icontains=courseName))
    jsonLocalData = loads(open('cc.txt','r').read())
    return render(request,'teacher/viewAssignmentTutor.html',{'allData':currentS,'jsonLocalData':jsonLocalData, 'prefill':prefill})

@login_required()
def teacherCalendar(request):   
    if request.session['type']=="Teacher":
        template = 'dashboard/Tutor-dashboard.html'    
    makepoint = MakeAppointment.objects.all()
    return render(request,'teacher/teachercalendar.html',{'template':template,'makepoint':makepoint})
