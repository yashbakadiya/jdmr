from django.shortcuts import render,HttpResponseRedirect,HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from teacher.models import enrollTutors
from students.models import AddStudentInst
from accounts.models import Teacher,Student,Institute
from batches.models import BatchTiming,BatchTimingTutor
from django.contrib import messages
from .models import *
from courses.models import Courses
from django.db.models import Q
from batches.models import BatchTiming
from json import loads
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from math import radians, sin, cos, asin, sqrt
from geopy.geocoders import Nominatim
import datetime  
from datetime import date 

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
                    if ins.courseName:
                        course = Courses.objects.get(courseName= ins.courseName)
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
                    if ins.batch:
                        batch = BatchTiming.objects.get(batchName= ins.batch)
                        batches.append(batch)
                return render(request,"Institute/institute.html",{"batches":batches,'student':student,"INST":INST[0],"template":"dashboard/base.html"})
            else:
                messages.warning(request,"Not Found")
                return render(request,"Institute/institute.html",{"template":"dashboard/base.html"})
    return HttpResponse("You are not Authenticated for this Page")

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
def searchCoachingCenter(request):
    jsonLocalData = loads(open('cc.txt','r').read())
    classlist = ['I','II','III','IV','V','VI','VII','VIII','IX','X','XI','XII','Other','Nursery']
    prefill={}
    if request.session['type']=="Student":
        centers = []
        if request.method == "POST":
            address = request.POST.get('loc','')
            distance = request.POST.get('distance','')
            Class = request.POST.get('className','')
            course = request.POST.get('subject','')

            prefill = {
                    "address":address,
                    "distance":distance,
                    "class":Class,
                    "course":course,
            }

            if distance=="":
                distance=0
            
            distance = float(distance)

            geolocator = Nominatim(user_agent="geoapiExercises")

            city = geolocator.geocode(address, timeout=None)
            if city:
                cityLat = city.latitude
                cityLng = city.longitude

            else:
                cityLat = float(request.POST.get('cityLat',''))
                cityLng = float(request.POST.get('cityLng',''))
            
            courses = Courses.objects.all()

            if(course):
                courses = courses.filter(Q(courseName__icontains=course))
            if(Class):
                courses = courses.filter(Q(forclass__icontains=Class))
            
            for cou in courses:
                inst = cou.intitute
                location = geolocator.geocode(inst.address, timeout=None)
                if location:
                    Lat = location.latitude
                    Lng = location.longitude

                else:
                    Lat = float(inst.latitude)
                    Lng = float(inst.longitude)

                if haversine(Lng,Lat,cityLng,cityLat) <=distance:
                    if inst not in centers:
                        centers.append(inst)
               
            # centers = zip(courses,centers2)
        return render(request, 'Institute/searchCoachingCenter.html',{'jsonLocalData':jsonLocalData,'centers':centers,"prefill":prefill})



@login_required(login_url="Login")
def ReviewInstitute(request,inst_id):
    user = User.objects.get(username=request.session['user'])
    user_type = request.session['type']
    show = False
    institute = Institute.objects.get(id=inst_id)
    if user_type == 'Student':
        student = Student.objects.get(user=user)
        if request.method == "POST" and not(InstituteRatings.objects.filter(student=student, institute=institute).exists()):
            rating =request.POST.get("rating","")
            comment = request.POST.get("comment","")
            data = InstituteRatings(
                    institute=institute,
                    student=student,
                    Review=comment,
                    Rating =rating)
            data.save()
        template = "dashboard/student-dashboard.html"
        if not InstituteRatings.objects.filter(student=student,institute=institute).exists():
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
    try:
        avgRating = sumRating/count
    except:
        avgRating = 0
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



@login_required()
def institutecalendar(request):
    if request.session['type']=="Institute":
        template = 'dashboard/institute-dashboard.html'
    
    return render(request,'Institute/institutecalendar.html',{'template':template})

# @login_required()
# def instCalendar(request):
#     if request.session['type']=="Institute":
#         template = 'dashboard/institute-dashboard.html'
        
#     return render(request,'Institute/instCalendar.html',{'template':template,})

def instCalendar(request):
    all_events = BatchTiming.objects.all()  
    template = 'dashboard/institute-dashboard.html'
    context = {
        
       
        "template":template ,
        "events":all_events

    }
    
    return render(request,'Institute/instCalendar.html',context )




def add_event(request):
    start = request.GET.get("start", None)
    end = request.GET.get("end", None)
    title = request.GET.get("title", None)
    event = Events(name=str(title), start=start, end=end)
    event.save()
    data = {}
    return JsonResponse(data)

def update(request):
    start = request.GET.get("start", None)
    end = request.GET.get("end", None)
    title = request.GET.get("title", None)
    id = request.GET.get("id", None)
    event = Events.objects.get(id=id)
    event.start = start
    event.end = end
    event.name = title
    event.save()
    data = {}
    return JsonResponse(data)


def remove(request):
    id = request.GET.get("id", None)
    event = Events.objects.get(id=id)
    event.delete()
    data = {}
    return JsonResponse(data)







@login_required()
def dateandbatch(request):
    if request.session['type']=='Institute':
        user = User.objects.get(username=request.session['user'])
        inst = Institute.objects.get(user=user)
        if request.method == 'POST':
            date = request.POST.get("selectdate") 
            print('date',date) 
            dat = (date.split('/'))
            month = dat[0]        
            day = int(dat[1])
            year =dat[2]  
            day_name = datetime.date(int(year), int(month), int(day)) 
            week = day_name.strftime("%A")
            print('week',week)
            obj = BatchTiming.objects.filter( days__icontains = week ) 

            print(day_name.strftime("%A"))
            # if day == 0 :
            #     obj = BatchTiming.objects.filter( days__icontains ='Sunday')                   
            # elif day == 1:
            #     obj = BatchTiming.objects.filter( days__icontains ='Monday')                 
            # elif day == 2:
            #     obj = BatchTiming.objects.filter( days__icontains ='Tuesday')               
            # elif day == 3:
            #     obj = BatchTiming.objects.filter( days__icontains ='Wednesday')
            # elif day == 4:
            #     obj = BatchTiming.objects.filter( days__icontains ='Thrusday')
            # elif day == 5:
            #     obj = BatchTiming.objects.filter( days__icontains ='Friday')
            # elif day == 6:
            #     obj = BatchTiming.objects.filter( days__icontains ='Saturday') 
            
      #  obj = BatchTiming.objects.filter( days__icontains ='Sunday')

    return render(request,'Institute/institutecalendar.html',{'obj':obj})
    

            
        
    



# @login_required()
# def institutecalendar(request):
#     if request.session['type']=="institute":
#         template = 'dashboard/student-dashboard.html'
#     elif request.session['type']=="Teacher":
#         template = 'dashboard/Tutor-dashboard.html'
#     return render(request,'students/studentcalendar.html',{'template':template})