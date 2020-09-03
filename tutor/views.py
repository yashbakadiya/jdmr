from django.shortcuts import render
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
import re
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_protect,csrf_exempt
from json import dumps,loads
from django.db.models import F
from django.core import serializers
import base64
from django.core.files.base import ContentFile
from .models import *
import random
import math
import json
from geopy.distance import distance as distanceBwAB
from geopy.geocoders import Nominatim
from datetime import datetime,timedelta
import pytz
from dateutil import parser,rrule
from collections import deque
from django.core.serializers.json import DjangoJSONEncoder
from django.forms.models import model_to_dict
from google.oauth2 import id_token
from google.auth.transport import requests
from django.core.mail import EmailMessage

CLIENT_ID = "450313289420-0sa8vg90n37pdek5nj49eufeia1j4918.apps.googleusercontent.com"
#CLIENT_ID = "1016598982512-u656rprh5a0f0j1jl0h00eq454kl1sla.apps.googleusercontent.com"

geolocator = Nominatim(user_agent="TutorSearch")

regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
allTimezones = pytz.all_timezones

def test1(request):
	# print(SignupTutorContinued.objects.get(sno=25).photo.url)
	request.session['data'] = 'working'
	request.session['number'] = 200
	# responce = render(request,'tutor/testing.html')
	responce = redirect("/test2")
	responce.set_cookie('test','dkw')
	return responce
def test2(request):
	# print(request.session.get('number'))
	# request = delSess(request,'number')
	# print(request.session.get('number'))
	return render(request,'tutor/noUserFound.html')

def landing(request):
	return redirect("/loginAll")

def delSess(request,var):
	try:
		del request.session[var]
	except:
		pass
	return request

def delCookie(responce,var):
	try:
		response.delete_cookie(var)
	except:
		pass
	return responce

def dashboardStudent(request):
	return render(request, 'tutor/dashboardStudent.html')

def dashboardTutor(request):
	return render(request, 'tutor/dashboardTutor.html')

def dashboard(request):
	return render(request, 'tutor/calendarCoaching.html')

def mainPage(request):
	return render(request, 'tutor/mainPage.html')

def loader(request):
	return render(request, 'tutor/loader.html')

def pageNotFound(request,dump):
	return HttpResponse("404 Page Not Found")

def logoutCoachingCentre(request):
	request = delSess(request,'CoachingCentre')
	responce = redirect('/loginCoachingCentre')
	responce.delete_cookie('CoachingCentreName')
	responce.delete_cookie('CoachingCentreAvatar')
	responce.delete_cookie('CoachingCentrePhoto')
	return responce

def logoutTutor(request):
	request = delSess(request,'Tutor')
	responce = redirect('/loginTutor')
	responce.delete_cookie('TutorName')
	responce.delete_cookie('TutorAvatar')
	responce.delete_cookie('TutorPhoto')
	return responce

def logoutStudent(request):
	request = delSess(request,'Student')
	responce = redirect('/loginStudent')
	responce.delete_cookie('StudentName')
	responce.delete_cookie('StudentAvatar')
	responce.delete_cookie('StudentPhoto')
	return responce


def loginCoachingCentre(request):
	if request.method=="POST":
		username = request.POST.get('username', '')
		password1 = request.POST.get('password1', '')
		rememberMe = request.POST.get('remember',False)
		print(request.POST)
		inst_names = SignupCoachingCentre.objects.values('instituteName', 'password','email','s_no','photo','avatar')
		for item in inst_names:
			if ((item['instituteName'] == username or item['email'] == username) and item['password'] == password1):
				login = LoginCoachingCentre(username=username,password=password1)
				login.save()
				request.session['CoachingCentre'] = item['s_no']
				print('url',item['photo'])
				responce = redirect('/dashboard')
				if rememberMe:
					responce.set_cookie('CoachingCentreName',item['instituteName'],max_age=60*60*24*365*10)
					responce.set_cookie('CoachingCentreAvatar',item['avatar'],max_age=60*60*24*365*10)
					responce.set_cookie('CoachingCentrePhoto',item['photo'],max_age=60*60*24*365*10)
				else:
					responce.set_cookie('CoachingCentreName',item['instituteName'])
					responce.set_cookie('CoachingCentreAvatar',item['avatar'])
					responce.set_cookie('CoachingCentrePhoto',item['photo'])
				return responce
		messages.error(request, "Invalid Credentials, Please try again")
	elif 'ajax' in request.POST:
		token = request.POST.get("token",False)
		if token:
			try:
				idinfo = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)
				userid = idinfo['sub']
				print(idinfo.values())
				email = idinfo['email']
				item = SignupCoachingCentre.objects.get(email=email)
				login = LoginCoachingCentre(username=item["username"],password=item["password1"])
				login.save()
				request.session['CoachingCentre'] = item['s_no']
				print('url',item['photo'])
				responce = redirect('/dashboard')
				responce.set_cookie('CoachingCentreName',item['instituteName'],max_age=60*60*24*365*10)
				responce.set_cookie('CoachingCentreAvatar',item['avatar'],max_age=60*60*24*365*10)
				responce.set_cookie('CoachingCentrePhoto',item['photo'],max_age=60*60*24*365*10)
			except ValueError:
				return redirect("/loginAll#coaching")

	return redirect('/loginAll#coaching')
	# return render(request, 'tutor/loginCoachingCentre.html')

def addCourses(request):
	if request.method=="POST":
		courseName = request.POST.get('courseName', '')
		count= AddCourses.objects.all().count()
		print(count)
		count=count+1
		name= request.POST.get('courseName', '')
		ch1=str("%03d" % count)
		ch2=str(name[0:2])
		cid=ch2+ch1
		forclass1 = request.POST.getlist('forclass', '')
		print(forclass1)
		forclass=', '.join(forclass1)
		cookieVAL = request.session.get('CoachingCentre')
		if(cookieVAL==None):
			return HttpResponse("<script>alert('Coaching Center is not logged in.')</script>")
		inst = SignupCoachingCentre.objects.get(s_no=cookieVAL)
		addCourses = AddCourses(courseName=courseName,cid=cid,forclass=forclass,coachingCentre= inst)
		addCourses.save()
		return redirect("/viewCourses/")
	return render(request, 'tutor/addCourses.html')

def teachingType(request):
	cookieVAL = request.session.get('CoachingCentre')
	if(cookieVAL==None):
		return HttpResponse("<script>alert('Coaching Center is not logged in.')</script>")
	inst = SignupCoachingCentre.objects.get(s_no=cookieVAL)
	courses = inst.AddCourses.all()
	jsonCources = {}
	for x in courses:
		jsonCources[x.courseName] = x.forclass.split(", ")
	params = {'courses':courses,'json':json.dumps(jsonCources)}
	print(params)
	if request.method=="POST":
		courseName = request.POST.get('courseName')
		forclass1 = request.POST.getlist('forclass', '')
		forclass=', '.join(forclass1)
		teachType1 = request.POST.getlist('check')
		teachType='\n'.join(teachType1)
		duration1 = request.POST.getlist('duration', '')
		duration='\n'.join(duration1)
		print(duration)
		timePeriod1 = request.POST.getlist('time', '')
		timePeriod='\n'.join(timePeriod1)
		print(timePeriod)
		# c_cid = AddCourses.objects.filter(Q(courseName__icontains=courseName)).values('cid')
		# l = list(c_cid)
		# a = l[0]
		# x = a["cid"]
		# print(x)
		# c_forclass = AddCourses.objects.filter(Q(courseName__icontains=courseName)).values('forclass')
		# lc = list(c_forclass)
		# ac = lc[0]
		# xc = ac["forclass"]
		# print(xc)
		alreadyExists = TeachingType.objects.filter(courseName=courseName,forclass=forclass,teachType=teachType,duration=duration,timePeriod=timePeriod)
		if(alreadyExists):
			return HttpResponse("""
					<script>
						alert('Teach Type already exists');
						window.location.href = "/teachingType";
					</script>
				""")
		course = inst.AddCourses.filter(Q(courseName=courseName))[0]
		teachingtype = TeachingType(course=course,courseName=courseName,forclass=forclass,teachType=teachType,duration=duration,timePeriod=timePeriod)
		teachingtype.save()
		# viewteachingtype = ViewTeachingType(cid=x,courseName=courseName,forclass=xc,teachType=teachType,durationInMonths=duration)
		# viewteachingtype.save()
		return redirect('/viewteachType/')
	return render(request, 'tutor/teachingType.html', params)

def viewteachType(request):
	teach = TeachingType.objects.all()
	print(teach)
	params = {'teach':teach}
	return render(request, 'tutor/viewteachType.html', params)

def editTeachingType(request,sno):
	cookieVAL = request.session.get('CoachingCentre')
	if(cookieVAL==None):
		return HttpResponse("<script>alert('Coaching Center is not logged in.')</script>")
	inst = SignupCoachingCentre.objects.get(s_no=cookieVAL)
	courses = inst.AddCourses.all()
	jsonCources = {}
	for x in courses:
		jsonCources[x.courseName] = x.forclass.split(", ")
	teach = TeachingType.objects.get(s_num=sno)
	params = {
		'courseName':teach.courseName,
		'forclass':teach.forclass.split(', '),
		'teachType':teach.teachType.split('\n'),
		'duration':teach.duration.split('\n'),
		'timePeriod':teach.timePeriod.split('\n')
	}
	params = {'teach':json.dumps(params),'courses':courses,'json':json.dumps(jsonCources)}
	if request.method=="POST":
		print(request.POST)
		courseName = request.POST.get('courseName')
		forclass1 = request.POST.getlist('forclass', '')
		forclass=', '.join(forclass1)
		teachType1 = request.POST.getlist('check')
		teachType='\n'.join(teachType1)
		duration1 = request.POST.getlist('duration', '')
		duration='\n'.join(duration1)
		print(duration)
		timePeriod1 = request.POST.getlist('time', '')
		timePeriod='\n'.join(timePeriod1)
		print(timePeriod)
		# c_cid = AddCourses.objects.filter(Q(courseName__icontains=courseName)).values('cid')
		# l = list(c_cid)
		# a = l[0]
		# x = a["cid"]
		# print(x)
		# c_forclass = AddCourses.objects.filter(Q(courseName__icontains=courseName)).values('forclass')
		# lc = list(c_forclass)
		# ac = lc[0]
		# xc = ac["forclass"]
		# print(xc)
		teach.courseName=courseName
		teach.forclass=forclass
		teach.teachType=teachType
		teach.duration=duration
		teach.timePeriod=timePeriod
		teach.save()
		# viewteachingtype = ViewTeachingType(cid=x,courseName=courseName,forclass=xc,teachType=teachType,durationInMonths=duration)
		# viewteachingtype.save()
		return redirect('/viewteachType/')
	return render(request, 'tutor/editTeachingType.html', params)

def searchteachType(request):
	if request.method=="POST":
		srch = request.POST.get('srh', '')
		if srch:
			match = TeachingType.objects.filter(Q(courseName__icontains=srch) |
											  Q(teachType__icontains=srch)
											  )
			if match:
				return render(request,'tutor/searchteachType.html', {'sr':match})
			else:
				messages.error(request,'no result found')
		else:
			return HttpResponseRedirect('/searchteachType/')
	return render(request, 'tutor/searchteachType.html')

def viewCourses(request):
	cookieVAL = request.session.get('CoachingCentre')
	if(cookieVAL==None):
		return HttpResponse("<script>alert('Coaching Center is not logged in.')</script>")
	inst = SignupCoachingCentre.objects.get(s_no=cookieVAL)
	courses = inst.AddCourses.all()
	print(courses)
	params = {'courses':courses}
	if request.method=="POST":
		print(request.POST)
		check = request.POST.getlist('check')
		print(check)
		archData = []
		m = AddCourses.objects.none()
		for i in check:
			if i:
				cn = AddCourses.objects.filter(Q(cid=i)).values('courseName')
				l = list(cn)
				a = l[0]
				x = a["courseName"]
				print(x)
				cc = AddCourses.objects.filter(Q(cid=i)).values('forclass')
				lc = list(cc)
				ac = lc[0]
				xc = ac["forclass"]
				print(xc)
				print(i)
				cookieVAL = request.session.get('CoachingCentre')
				if(cookieVAL==None):
					return HttpResponse("<script>alert('Coaching Center is not logged in.')</script>")
				inst = SignupCoachingCentre.objects.get(s_no=cookieVAL)
				arcCourses = ArchiveCourses(crid=i,crName=x,crclass=xc,coachingCentre = inst)
				arcCourses.save()
				match = AddCourses.objects.filter(Q(cid=i))
				print(match)
				m = m.union(match)
				try:
					temp = inst.AddCourses.get(Q(cid=i))
					archTemp = [temp.cid,temp.courseName,temp.forclass]
					archData.append(archTemp)
					temp.delete()
				except Exception as e:
					print(270,e)

		# param = {'course':m}
		# print(param)
		return render(request,'tutor/archiveCourse.html', {'param':archData})
	return render(request, 'tutor/viewCourses.html', params)

def search(request):
	if request.method=="POST":
		srch = request.POST.get('srh', '')
		cookieVAL = request.session.get('CoachingCentre')
		if(cookieVAL==None):
			return HttpResponse("<script>alert('Coaching Center is not logged in.')</script>")
		inst = SignupCoachingCentre.objects.get(s_no=cookieVAL)
		if srch:
			match = inst.AddCourses.filter(Q(courseName__icontains=srch) |
											  Q(forclass__icontains=srch) |
											  Q(cid__icontains=srch)
											  )
			print(match)
			if match:
				return render(request,'tutor/search.html', {'sr':match})
			else:
				messages.error(request,'no result found')
		else:
			return HttpResponseRedirect('/search/')
	return render(request, 'tutor/search.html')

# def deleteCourse(request,s_num):
#         count= AddCourses.objects.all().count()
#         count_1 = str("%03d" % count)
#         count1 = int(count_1)
#         print(count1) #10

#         dc = AddCourses.objects.get(s_num=s_num)
#         dca = AddCourses.objects.filter(Q(s_num__icontains=s_num)).values('cid')
#         a = list(dca)
#         dcar = a[0]["cid"] #ab002
#         sliceid = dcar[2:5]
#         slice_id = int(sliceid)
#         dcab = ArchiveCourses.objects.filter(Q(crid__icontains=dcar)).values('crid')
#         if dcab:
#             b = list(dcab)
#             dcarb = b[0]["crid"]
#             arc = ArchiveCourses.objects.get(crid=dcarb)
#             if dcar == dcarb:
#                 arc.delete()
#         dc.delete()

#         if slice_id != count1:
#             slice_id = slice_id + 1
#             count1 = count1 + 1
#             print(slice_id) #3
#             print(count1) #11
#             for i in range(slice_id,count1):
#                 s = i-1
#                 print(s)
#                 c1 = str("%03d" % s)
#                 print(c1) #002
#                 c3 = str("%03d" % i)
#                 print(c3) #003
#                 acn = AddCourses.objects.filter(Q(cid__icontains=c3)).values('courseName')
#                 print(acn)
#                 bcn = list(acn)
#                 cn = bcn[0]["courseName"]
#                 c2 = str(cn[0:2])
#                 print(c2) #ca
#                 k = c2 + c1
#                 print(k) #ca002
#                 AddCourses.objects.filter(Q(cid__icontains=c3)).update(cid = k)
#         return redirect("/viewCourses/")

def deleteCourse(request,s_num):
	cookieVAL = request.session.get('CoachingCentre')
	if(cookieVAL==None):
		return HttpResponse("<script>alert('Coaching Center is not logged in.')</script>")
	inst = SignupCoachingCentre.objects.get(s_no=cookieVAL)
	delObj = inst.AddCourses.get(s_num=s_num)
	delObj.delete()
	# try:
	# 	cookieVAL = request.session.get('CoachingCentre')
	# 	if(cookieVAL==None):
	# 		return HttpResponse("<script>alert('Coaching Center is not logged in.')</script>")
	# 	inst = SignupCoachingCentre.objects.get(s_no=cookieVAL)
	# 	delObj = inst.AddCourses.get(s_num=s_num)
	# 	delObj.delete()
	# except Exception as e:
	# 	print(e)

	return redirect('/viewCourses')


def deleteArchiveCourse(request,s_num):
	try:
		cookieVAL = request.session.get('CoachingCentre')
		if(cookieVAL==None):
			return HttpResponse("<script>alert('Coaching Center is not logged in.')</script>")
		inst = SignupCoachingCentre.objects.get(s_no=cookieVAL)
		delObj = inst.ArchiveCourses.get(sn=s_num)
		delObj.delete()
	except Exception as e:
		print(e)

	return redirect('/archiveCourseList')

def editCourse(request,s_num):
	cookieVAL = request.session.get('CoachingCentre')
	if(cookieVAL==None):
		return HttpResponse("<script>alert('Coaching Center is not logged in.')</script>")
	inst = SignupCoachingCentre.objects.get(s_no=cookieVAL)
	a = inst.AddCourses.filter(Q(s_num__icontains=s_num)).values('courseName','forclass')
	b = list(a)
	c = b[0]["courseName"]
	d = json.dumps(b[0]["forclass"].split(', '))
	print(c)
	l = inst.AddCourses.filter(Q(s_num__icontains=s_num)).values('cid')
	x = list(l)
	y = x[0]["cid"]
	z = str(y[2:5])
	print(z) #002
	params = {'course':c,'class':d}
	if request.method=="POST":
		courseName = request.POST.get('cName', '')
		x=courseName[0:2] #ma
		k = x + z
		forclass1 = request.POST.getlist('forclass', '')
		print(forclass1)
		forclass=', '.join(forclass1)
		inst.AddCourses.filter(s_num=s_num).update(cid=k,courseName=courseName,forclass=forclass,coachingCentre=inst)
		return redirect("/viewCourses/")
	return render(request, 'tutor/editCourse.html', params)

def archiveCourse(request):
	return render(request, 'tutor/archiveCourse.html', params)

def archiveCourseList(request):
	cookieVAL = request.session.get('CoachingCentre')
	if(cookieVAL==None):
		return HttpResponse("<script>alert('Coaching Center is not logged in.')</script>")
	inst = SignupCoachingCentre.objects.get(s_no=cookieVAL)
	if(request.method=='POST'):
		entries = request.POST.getlist('undo')
		for x in entries:
			obj = ArchiveCourses.objects.get(sn=x)
			newObj = AddCourses(
					cid         = obj.crid,
					courseName  = obj.crName,
					forclass    = obj.crclass,
					coachingCentre = obj.coachingCentre
				)
			newObj.save()
			obj.delete()
	course = inst.ArchiveCourses.all()
	params = {'course':course}
	return render(request, 'tutor/archiveCourseList.html', params)

def signupCoachingCentre(request):
	print('testing',request.method)
	if request.method=="POST":
		instituteName = request.POST.get('instituteName', '')
		count= SignupCoachingCentre.objects.all().count()
		count=count+1
		name= request.POST.get('instituteName', '')
		ch1=str("%04d" % count)
		ch2=str(name[0:2])
		instituteCode=ch2+ch1
		email = request.POST.get('email', '')
		password = request.POST.get('password', '')
		phone = request.POST.get('phone', '')
		loaction = request.POST.get('loc')
		latitude = request.POST.get('cityLat')
		longitude = request.POST.get('cityLng')
		confpassword = request.POST.get('confpassword')
		if password != confpassword:
			messages.error(request, "Passwords do not match")
			return redirect('/signupCoachingCentre/')
		elif len(phone) != 10:
			messages.error(request, "Phone Number must be 10 digits")
			return redirect('/signupCoachingCentre/')
		elif phone.isdigit() == False:
			messages.error(request, "Phone Number must be numeric")
			return redirect('/signupCoachingCentre/')
		else:
			signupCoachingCentre = SignupCoachingCentre(
				instituteName=instituteName,
				instituteCode=instituteCode,
				email=email,
				password=password,
				phone=phone,
				location=loaction,
				latitude=latitude,
				longitude=longitude
			)
			signupCoachingCentre.save()
			return redirect('/loginCoachingCentre/')
	return render(request, 'tutor/signupCoachingCentre.html')

def viewteachingType(request):
	teach = ViewTeachingType.objects.all()
	params = {'courses':teach}
	return render(request, 'tutor/viewteachingType.html', params)

def loginTutor(request):
	if request.method=="POST":
		username = request.POST.get('username', '')
		password1 = request.POST.get('password1', '')
		inst_names = SignupTutor.objects.values('username', 'password','sno')
		rememberMe = request.POST.get('remember',False)
		max_age = None
		if rememberMe:
			max_age = 60*60*24*365*10
		for item in inst_names:
			if item['username'] == username and item['password'] == password1:
				request.session['Tutor'] = item['sno']
				print(item['sno'])
				subDetails = SignupTutor.objects.get(username=username,password=password1,sno=item['sno']).signupTutorContinued.all()
				if(len(subDetails)>0):
					print(subDetails)
					responce = redirect('/dashboardTutor/')
					responce.set_cookie('TutorName',item['username'],max_age=max_age)
					responce.set_cookie('TutorAvatar',SignupTutor.objects.get(username=username,password=password1,sno=item['sno']).signupTutorContinued.all()[len(subDetails)-1].avatar,max_age=max_age)
					responce.set_cookie('TutorPhoto',SignupTutor.objects.get(username=username,password=password1,sno=item['sno']).signupTutorContinued.all()[len(subDetails)-1].photo,max_age=max_age)
					return responce
				else:
					responce = redirect(f'/signupTutorContinued/{item["sno"]}')
					responce.set_cookie('TutorName',item['username'],max_age=max_age)
					# responce.set_cookie('TutorAvatar',item['avatar'])
					# responce.set_cookie('TutorPhoto',item['photo'])
					return responce
		messages.error(request, "Invalid Credentials, Please try again")
	elif 'ajax' in request.POST:
		token = request.POST.get("token",False)
		if token:
			try:
				max_age = 60*60*24*365*10

				idinfo = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)
				userid = idinfo['sub']
				print(idinfo.values())
				email = idinfo['email']
				item = SignupTutor.objects.get(email= email)
				request.session['Tutor'] = item['sno']
				print(item['sno'])
				subDetails = item.signupTutorContinued.all()
				if(len(subDetails)>0):
					print(subDetails)
					responce = redirect('/dashboardTutor/')
					responce.set_cookie('TutorName',item['username'],max_age=max_age)
					responce.set_cookie('TutorAvatar',SignupTutor.objects.get(username=username,password=password1,sno=item['sno']).signupTutorContinued.all()[len(subDetails)-1].avatar,max_age=max_age)
					responce.set_cookie('TutorPhoto',SignupTutor.objects.get(username=username,password=password1,sno=item['sno']).signupTutorContinued.all()[len(subDetails)-1].photo,max_age=max_age)
					return responce
				else:
					responce = redirect(f'/signupTutorContinued/{item["sno"]}')
					responce.set_cookie('TutorName',item['username'],max_age=max_age)
					# responce.set_cookie('TutorAvatar',item['avatar'])
					# responce.set_cookie('TutorPhoto',item['photo'])
					return responce
			except ValueError:
				return redirect("/loginAll#tutor")
	return redirect('/loginAll#tutor')
	# return render(request,'tutor/loginTutor.html')

def signupTutor(request):
	errors = []
	prefil = {}
	if request.method=="POST":
		firstName = request.POST.get('firstName', '')
		count= SignupTutor.objects.all().count()
		count=count+1
		name= request.POST.get('firstName', '')
		ch1=str("%04d" % count)
		ch2=str(name[0:2])
		tutorCode=ch2+ch1
		lastName = request.POST.get('lastName', '')
		email = request.POST.get('email', '')
		username = email
		password = request.POST.get('password', '')
		distance = request.POST.get('distance','')
		latitude = request.POST.get('cityLat')
		longitude = request.POST.get('cityLng')
		phone = request.POST.get('phone', '')
		location = request.POST.get('loc', '')
		prefil = {
			"username":username,
			"firstName":firstName,
			"lastName":lastName,
			"email":email,
			"distance":distance,
			"phone":phone,
		}

		if firstName.isalpha() == False | lastName.isalpha() == False:
			errors.append("Name must be alphabetical")
		if len(phone) != 10:
			errors.append("Phone Number must be 10 digits")
		if phone.isdigit() == False:
			errors.append("Phone Number must be numeric")
		if distance.isdigit() == False:
			errors.append("Distance must be numeric")
		if(errors):
			return render(request, 'tutor/signupTutor.html',{"errors":errors,"prefil":prefil})
		else:
			signupTutor = SignupTutor(
				username=username,
				firstName=firstName,
				tutorCode=tutorCode,
				lastName=lastName,
				email=email,
				password=password,
				distance=distance,
				phone=phone,
				location=location,
				latitude=latitude,
				longitude=longitude
			)
			signupTutor.save()
		return redirect('/loginTutor/')
	return render(request, 'tutor/signupTutor.html')
def signupTutorContinued(request,sno):
	if(request.method=='POST'):
		print(request.POST)

		# base signup class
		baseModel = SignupTutor.objects.get(sno=sno)
		# creating data object
		forclass = request.POST.getlist('cn_combined')
		forclass = ";".join(forclass)
		courseName = request.POST.getlist('ctn_combined')
		courseName = ";".join(courseName)
		availability = request.POST.getlist('availability')
		availability = ", ".join(availability)
		image = request.POST.get('photo')
		obj = SignupTutorContinued(
				base            = baseModel,
				availability    = request.POST.getlist('availability'),
				qualification   = request.POST.get('qualification'),
				description     = request.POST.get('description'),
				experience      = request.POST.get('experience'),
				gender          = request.POST.get('gender'),
				courseName      = courseName,
				forclass        = forclass,
				fees            = float(request.POST.get('fees',1.1)),
				freeDemo        = request.POST.get('fda',0)
			)
		if(image):
			if(image.isdigit()):
				print('asdd',image)
				obj.avatar = image
				obj.photo = None
			else:
				f,img = image.split(';base64,')
				ext = f.split('/')[-1]
				image = ContentFile(base64.b64decode(img),name='temp.'+ext)
				obj.avatar = 0
				obj.photo = image
		obj.save()
		responce = redirect('/dashboardTutor/')
		responce.set_cookie('TutorAvatar',obj.avatar)
		responce.set_cookie('TutorPhoto',obj.photo)
		return responce
	# teaching type data
	data = TeachingType.objects.values_list('courseName','forclass','teachType')
	processed_data = {}
	# processing data into usable form
	for x in data:
		processed_data[x[0]] = [x[1].split(", "),x[2].split("\n")]
	jsonLocalData = loads(open('cc.txt','r').read())
	return render(
		request,
		'tutor/signupTutorContinued.html',
		{
			"data":TeachingType.objects.all(),
			"jsdata":dumps(processed_data),
			'jsonLocalData':jsonLocalData
		}
	)
def testing(request):
	return HttpResponse("<script>alert('hello')</script>")

def addTutors(request):
	errors = []
	if request.method=="POST":
		firstName = request.POST.get('firstName', '')
		lastName = request.POST.get('lastName', '')
		email = request.POST.get('email', '')
		phone = request.POST.get('phone', '')
		password = phone
		distance = request.POST.get('distance',0)
		username = email
		count= SignupTutor.objects.all().count()
		count=count+1
		name= request.POST.get('firstName', '')
		ch1=str("%04d" % count)
		ch2=str(name[0:2])
		tutorCode=ch2+ch1

		location = request.POST.get('schoolName', '')
		lat = request.POST.get('cityLat', 1)
		lng = request.POST.get('cityLng', 1)

		if firstName.isalpha() == False | lastName.isalpha() == False:
			errors.append("Name must be alphabetical")
		if len(phone) != 10:
			errors.append("Phone Number must be 10 digits")
		if phone.isdigit() == False:
			errors.append("Phone Number must be numeric")
		if distance.isdigit() == False:
			errors.append("Distance must be numeric")
		if SignupTutor.objects.filter(email=email).exists():
			errors.append("Email Already Exists")
		if SignupTutor.objects.filter(phone=phone).exists():
			errors.append("Phone No is Already Registered")
		if(errors):
			return render(request, 'tutor/signupTutor.html',{"errors":errors})
		else:
			signupTutor = SignupTutor(
				username=username,
				firstName=firstName,
				tutorCode=tutorCode,
				lastName=lastName,
				email=email,
				password=password,
				distance=distance,
				phone=phone,
				location=location,
				latitude=lat,
				longitude=lng
			)
			cookieVAL = request.session.get('CoachingCentre')
			if(cookieVAL==None):
				return HttpResponse("<script>alert('Coaching Center is not logged in.')</script>")
			signupTutor.save()
			# sTutor = SignupTutor.objects.get(sno=int(request.GET.get('id')))
			inst = SignupCoachingCentre.objects.get(s_no=cookieVAL)
			match = enrollTutors(
				signUp          = signupTutor,
				instituteName   = inst.instituteName,
				instituteCode   = inst.instituteCode
			)
			match.save()
			ctn = request.POST.getlist('ctn_combined')
			cn = request.POST.getlist('cn_combined')
			ttn = request.POST.getlist('ttn_combined')
			ttn = [x.replace("\r","") for x in ttn]
			availability = request.POST.get('availability')
			if(availability=='weekly'):
				availability=1
			elif(availability=='weekend'):
				availability=2
			elif(availability=='both'):
				availability=3
			else:
				print('availability error')
				availability=0
			for x in range(len(ttn)):
				# signup_tutor = SignupTutor.objects.get(sno=sno)
				# cid = SignupCoachingCentre.objects.get(s_no=int(cookieVAL))
				savTut = AddTutorsInst(
						username=match,
						cid = inst ,
						courseTaught = ctn[x] ,
						forclass = cn[x] ,
						teachType = ttn[x] ,
						availability = availability
					)
				try:
					savTut.save()
				except:
					signupTutor.delete()
					match.delete()
					return redirect("/addTutors")
			return HttpResponse("""
					<script>
						alert('Student Added Sucessfully');
						window.location.href = "/addTutors";
					</script>
				""")
	data = TeachingType.objects.values_list('courseName','forclass','teachType')
	processed_data = {}
	for x in data:
		processed_data[x[0]] = [x[1].split(", "),x[2].split("\n")]
	return render(
		request,
		'tutor/addTutors.html',
		{
			"data":TeachingType.objects.all(),
			"jsdata":dumps(processed_data)
		}
	)

@csrf_protect
def addTutorWork(request):
	cookieVAL = request.session.get('CoachingCentre')
	if(cookieVAL==None):
		return HttpResponse("<script>alert('Coaching Center is not logged in.')</script>")
	inst = SignupCoachingCentre.objects.get(s_no=cookieVAL)
	courses = inst.AddCourses.all()
	params = {'courses':courses}
	if request.method=="POST":
		tutorname = request.POST.get('tutorName', '')
		print(tutorname)
		email = request.POST.get('email', '')
		print(email)
		phone = request.POST.get('phone', '')
		print(phone)
		courseTaught1 = request.POST.getlist('courseName', '')
		print(courseTaught1)
		forclass1 = request.POST.getlist('forclass', '')
		print(forclass1)
		teachType1 = request.POST.getlist('check')
		print(teachType1)
		availability = request.POST.getlist('radio', '')
		print(availability)
	return render(request, 'tutor/addTutorWork.html',params)

def searchTutor(request):
	if request.method=="POST":
		srch = request.POST.get('srh', '')
		if srch:
			match = AddTutorsInst.objects.filter(Q(tutorname__icontains=srch) |
											  Q(courseTaught__icontains=srch) |
											  Q(forclass__icontains=srch) |
											  Q(availability__icontains=srch) |
											  Q(teachType__icontains=srch)
											  )
			print(match)
			if match:
				return render(request,'tutor/searchTutor.html', {'sr':match})
			else:
				messages.error(request,'no result found')
		else:
			return HttpResponseRedirect('/searchTutor/')
	return render(request, 'tutor/searchTutor.html')

def searchUserTutor(request):
	if request.method=="POST":
		# get logged in coaching center
		coachingCtr = request.session.get('CoachingCentre')
		# if coaching center is not logged in then redirecr
		if not coachingCtr:
			return HttpResponse("<script>alert('Coaching Center is not logged in');window.location.href = '/loginCoachingCentre';</script>")
		# data to be searched
		srch = request.POST.get('srh', '')
		if srch:
			print(srch)
			#filter all matching queries
			match = SignupTutor.objects.filter(Q(username__icontains=srch) |
												Q(email__icontains=srch)
											  )
			# currently signed in coaching center
			print(match)
			currentCC = SignupCoachingCentre.objects.get(s_no=coachingCtr)
			cleanedData = []
			# iterating over all matching queres
			for x in match:
				# iteration over all mathing enrollTutors objects
				for y in x.enrollTutors.all():
					if(currentCC.instituteCode == y.instituteCode):
						break
				# if for any enrollTutors object corresponding
				# to SignupTutor object contains the institute
				# code for currently signed in institute then it
				# is not concidered
				else:
					cleanedData.append(x)
			if len(match):
				return render(request,'tutor/searchUserTutor.html', {'sr':cleanedData})
			else:
				messages.error(request,'no result found')
				return redirect("/addTutors#noTutor")
		else:
			return HttpResponseRedirect('/searchUserTutor/')
	return render(request, 'tutor/searchUserTutor.html')

def enrollTutor(request):
	if request.method=='GET':
		cookieVAL = request.session.get('CoachingCentre')
		sTutor = SignupTutor.objects.get(sno=int(request.GET.get('id',0)))
		inst = SignupCoachingCentre.objects.get(s_no=cookieVAL)
		match = enrollTutors(
				signUp          = sTutor,
				instituteName   = inst.instituteName,
				instituteCode   = inst.instituteCode
			)
		match.save()
		print(match.sno)
	return HttpResponse(match.sno)

def addTutorInst(request,sno):
	if(request.method=='POST'):
		print(request.POST)
		ctn = request.POST.getlist('ctn_combined')
		cn = request.POST.getlist('cn_combined')
		ttn = request.POST.getlist('ttn_combined')
		ttn = [x.replace("\r","") for x in ttn]
		print(cn)
		print(ttn)
		print(ctn)
		print(len(ttn))
		availability = request.POST.get('availability')
		print('a',availability)
		for x in range(len(ttn)):
			print(x)
			connection = enrollTutors.objects.get(sno=sno)
			cookieVAL = request.session.get('CoachingCentre')
			if(not cookieVAL):
				return HttpResponse("You are not logged in!")
			cid = SignupCoachingCentre.objects.get(s_no=int(cookieVAL))
			print('aba',availability)
			if(availability=='weekly'):
				availability=1
			elif(availability=='weekend'):
				availability=2
			elif(availability=='both'):
				availability=3
			else:
				print('availability',availability)
			savTut = AddTutorsInst(
					username=connection,
					cid = cid ,
					courseTaught = ctn[x] ,
					forclass = cn[x] ,
					teachType = ttn[x] ,
					availability = availability
				)
			savTut.save()
		return redirect("/dashboard")
	data = TeachingType.objects.values_list('courseName','forclass','teachType')
	processed_data = {}
	for x in data:
		processed_data[x[0]] = [x[1].split(", "),x[2].split("\n")]
	return render(
		request,
		'tutor/addTutorInst.html',
		{
			"data":TeachingType.objects.all(),
			"jsdata":dumps(processed_data)
		}
	)

def viewTutorInst(request):
	tutor = AddTutorsInst.objects.all()
	params = {'tutor':tutor}
	return render(request, 'tutor/viewTutorInst.html', params)

def viewTutors(request):
	tutors = enrollTutors.objects.all()
	params = {'tutors':tutors}
	if request.method=="POST":
		print(request.POST)
		# contains SignupTutor sno
		# put - for empty
		check = request.POST.getlist('check')
		for x in check:
			sno = x.split('|')[0]
			instName = x.split('|')[1]
			instCode = x.split('|')[2]
			print(sno)
			tutObj = SignupTutor.objects.get(sno=sno)
			for contObj in tutObj.signupTutorContinued.all():
				pass
			else:
				contObj = SignupTutorContinued()
				contObj.save()

			try:
				entObj = tutObj.enrollTutors.all()[0]
			except:
				entObj = enrollTutors()
				entObj.save()

			print(entObj)
			try:
				atiObj = entObj.AddTutorsInst.all()[0]
			except:
				atiObj = AddTutorsInst()
				atiObj.save()
			print(atiObj)
			print(atiObj.courseTaught)
			print(atiObj.forclass)
			print(atiObj.availability)
			print(atiObj.teachType)

			archObj = ArchiveTutors(
						tutorCode = tutObj.tutorCode ,
						username = tutObj.username ,
						firstName = tutObj.firstName ,
						lastName = tutObj.lastName ,
						email = tutObj.email ,
						password = tutObj.password ,
						distance = tutObj.distance ,
						location = tutObj.location ,
						phone = tutObj.phone ,
						latitude = tutObj.latitude ,
						longitude = tutObj.longitude ,

						availability = atiObj.availability ,
						qualification = contObj.qualification ,
						experience = contObj.experience ,
						description = contObj.description ,
						gender = contObj.gender ,
						courseName = atiObj.courseTaught ,
						forclass = atiObj.forclass ,
						fees = contObj.fees ,
						photo = contObj.photo ,
						freeDemo = contObj.freeDemo ,
						avatar = contObj.avatar ,
						instituteName = instName,
						instituteCode = instCode,
						teachType = atiObj.teachType
					)
			archObj.save()
			tutObj.delete()
			contObj.delete()
			entObj.delete()
		return redirect('/archiveTutorList')
		# return render(request,'tutor/archiveTutor.html', param)
	return render(request, 'tutor/viewTutors.html', params)

def deleteTutor(request,sno):
	print('delete',sno)
	delObj  = enrollTutors.objects.get(sno=sno)
	delObj.delete()
	return redirect("/viewTutors/")


def editTutorMini(request,sno):
	if(request.method=='POST'):
		ctn = request.POST.getlist('ctn_combined')
		cn = request.POST.getlist('cn_combined')
		ttn = request.POST.getlist('ttn_combined')
		ttn = [x.replace("\r","") for x in ttn]
		availability = request.POST.get('availability')
		for x in range(len(ttn)):
			signup_tutor = SignupTutor.objects.get(sno=sno)
			cookieVAL = request.session.get('CoachingCentre')
			if(not cookieVAL):
				return HttpResponse("You are not logged in!")
			cid = SignupCoachingCentre.objects.get(s_no=int(cookieVAL))
			if(availability=='weekly'):
				availability=1
			elif(availability=='weekend'):
				availability=2
			elif(availability=='both'):
				availability=3
			else:
				print('availability error')
				availability=0
			savTut = AddTutorsInst(
					username=signup_tutor,
					cid = cid ,
					courseTaught = ctn[x] ,
					forclass = cn[x] ,
					teachType = ttn[x] ,
					availability = availability
				)
			savTut.save()
		NewUsername = request.POST.get("NewUsername")
		NewEmail = request.POST.get("NewEmail")
		NewPassword = request.POST.get("NewPassword")
		NewPhone = request.POST.get("NewPhone")
		updateTutorObj = SignupTutor.objects.get(sno=sno)
		updateTutorObj.username = NewUsername
		updateTutorObj.email = NewEmail
		updateTutorObj.password = NewPassword
		updateTutorObj.phone = NewPhone
		updateTutorObj.save()
		return redirect("/dashboard")
	data = TeachingType.objects.values_list('courseName','forclass','teachType')
	processed_data = {}
	for x in data:
		processed_data[x[0]] = [x[1].split(", "),x[2].split("\n")]
	return render(
		request,
		'tutor/editTutorMini.html',
		{
			"data":TeachingType.objects.all(),
			"jsdata":dumps(processed_data),
			"tutorBaseData":SignupTutor.objects.get(sno=sno)
		}
	)



def editTutor(request,sno):
	if(request.method=='POST'):
		print(request.POST)
		ctn = request.POST.getlist('ctn_combined')
		cn = request.POST.getlist('cn_combined')
		ttn = request.POST.getlist('ttn_combined')
		ttn = [x.replace("\r","") for x in ttn]
		availability = request.POST.get('availability')
		if(availability=='weekly'):
			availability=1
		elif(availability=='weekend'):
			availability=2
		elif(availability=='both'):
			availability=3
		else:
			print('availability error')
			availability=0

		signup_tutor = SignupTutor.objects.get(sno=sno).enrollTutors.all()[0].AddTutorsInst.all()
		usn = SignupTutor.objects.get(sno=sno).enrollTutors.all()[0]
		for x in signup_tutor:
			x.delete()
		for x in range(len(ttn)):
			signup_tutor = SignupTutor.objects.get(sno=sno)
			cookieVAL = request.session.get('CoachingCentre')
			if(not cookieVAL):
				return HttpResponse("You are not logged in!")
			cid = SignupCoachingCentre.objects.get(s_no=int(cookieVAL))
			savTut = AddTutorsInst(
					username=usn,
					cid = cid ,
					courseTaught = ctn[x] ,
					forclass = cn[x] ,
					teachType = ttn[x] ,
					availability = availability
				)
			savTut.save()
		NewUsername = request.POST.get("NewUsername")
		NewEmail = request.POST.get("NewEmail")
		NewPassword = request.POST.get("NewPassword")
		NewPhone = request.POST.get("NewPhone")
		updateTutorObj = SignupTutor.objects.get(sno=sno)
		updateTutorObj.username = NewUsername
		updateTutorObj.email = NewEmail
		updateTutorObj.password = NewPassword
		updateTutorObj.phone = NewPhone
		updateTutorObj.save()
		return redirect("/dashboard")
	tutorData = SignupTutor.objects.get(sno=sno).enrollTutors.all()[0].AddTutorsInst.all()
	cleantutorData = []
	for x in tutorData:
		temp = {}
		temp["courseTaught"] = x.courseTaught
		temp["forclass"] = x.forclass.split(", ")
		temp["teachType"] = x.teachType.split("\n")
		temp["availability"] = x.availability.to_eng_string()
		cleantutorData.append(temp)
	data = TeachingType.objects.values_list('courseName','forclass','teachType')
	processed_data = {}
	for x in data:
		processed_data[x[0]] = [x[1].split(", "),x[2].split("\n")]
	return render(
		request,
		'tutor/editTutor.html',
		{
			"tutorData":cleantutorData,
			"jsontutorData":dumps(cleantutorData),
			"data":TeachingType.objects.all(),
			"jsdata":dumps(processed_data),
			"tutorBaseData":SignupTutor.objects.get(sno=sno)
		}
	)

def archiveTutor(request):
	# return render(request, 'tutor/archiveTutor.html')
	return redirect('/archiveTutorList')

# correct one
def archiveTutorList(request):
	tutor = ArchiveTutors.objects.all()
	params = {'tutor':tutor}
	return render(request, 'tutor/archiveTutorList.html', params)

def deleteArchiveTutorList(request,sno):
	try:
		obj = ArchiveTutors.objects.get(sno=sno)
		obj.delete()
	except Exception as e:
		print(e)
	return redirect('/archiveTutorList')

def undoArchiveTutor(request):
	if(request.method=='POST'):
		idList = request.POST.getlist('check')
		print(idList)
		for x in idList:
			o = ArchiveTutors.objects.get(sno=x)
			print(o)
			o1 = SignupTutor(
					tutorCode = o.tutorCode,
					username =  o.username,
					firstName =  o.firstName,
					lastName =  o.lastName,
					email = o.email ,
					password =  o.password,
					distance =  o.distance,
					location =  o.location,
					phone = o.phone,
					latitude =  o.latitude,
					longitude =  o.longitude
				)
			o1.save()
			o2 = SignupTutorContinued(
					base = o1,
					availability = o.availability,
					qualification = o.qualification,
					experience = o.experience,
					description = o.description,
					gender = o.gender,
					courseName = o.courseName,
					forclass = o.forclass,
					fees = o.fees,
					photo = o.photo,
					freeDemo = o.freeDemo,
					avatar = o.avatar,
				)
			o2.save()
			o3 = enrollTutors(
					signUp = o1,
					instituteName = o.instituteName,
					instituteCode = o.instituteCode,
				)
			o3.save()
			coachcObj = SignupCoachingCentre.objects.get(instituteCode=o.instituteCode)
			o4 = AddTutorsInst(
					username = o3,
					cid = coachcObj,
					courseTaught = o.courseName,
					forclass = o.forclass,
					teachType = o.teachType,
					availability = o.availability,
				)
			o4.save()
			o.delete()
	return redirect('/archiveTutorList')



def loginStudent(request):
	if request.method=="POST":
		print(request.POST)
		username = request.POST.get('username', '')
		password1 = request.POST.get('password1', '')
		rememberMe = request.POST.get('remember',False)
		max_age = None
		if rememberMe:
			max_age = 60*60*24*365*10
		inst_names = SignupStudent.objects.values('firstName', 'password', 'snum','avatar','photo')
		for item in inst_names:
			print(item,username,password1)
			if item['firstName'] == username and item['password'] == password1:
				request.session['Student'] = item['snum']
				responce = HttpResponse("<script>setTimeout(function(){window.location.href='/dashboardStudent/'},0000);</script>")
				responce.set_cookie('StudentName',item['firstName'], max_age = max_age)
				responce.set_cookie('StudentAvatar',item['avatar'], max_age = max_age)
				responce.set_cookie('StudentPhoto',item['photo'], max_age = max_age)
				return responce
		messages.error(request, "Invalid Credentials, Please try again")
	elif 'ajax' in request.POST:
		token = request.POST.get("token",False)
		if token:
			try:
				max_age = 60*60*24*365*10

				idinfo = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)
				userid = idinfo['sub']
				print(idinfo.values())
				email = idinfo['email']
				item = SignupStudent.objects.get(email= email)
				request.session['Student'] = item['snum']
				responce = HttpResponse("<script>setTimeout(function(){window.location.href='/dashboardStudent/'},0000);</script>")
				responce.set_cookie('StudentName',item['firstName'], max_age = max_age)
				responce.set_cookie('StudentAvatar',item['avatar'], max_age = max_age)
				responce.set_cookie('StudentPhoto',item['photo'], max_age = max_age)
				return responce
			except ValueError:
				return redirect("/loginAll#student")
	return redirect('/loginAll#student')
	# return render(request, 'tutor/loginStudent.html')

def signupStudent(request):
	schools = School.objects.all()
	school_list = list(map(str,schools))
	if request.method=="POST":
		firstName = request.POST.get('firstName', '')
		count= SignupStudent.objects.all().count()
		count=count+1
		name= request.POST.get('firstName', '')
		ch1=str("%04d" % count)
		ch2=str(name[0:2])
		studentCode=ch2+ch1
		lastName = request.POST.get('lastName', '')
		email = request.POST.get('email', '')
		latitude = request.POST.get('cityLat')
		longitude = request.POST.get('cityLng')
		username = email
		password = request.POST.get('password', '')
		phone = request.POST.get('phone', '')
		location = request.POST.get('loc')
		if firstName.isalpha() == False | lastName.isalpha() == False :
			messages.error(request, "Name must be alphabetical")
			return redirect('/signupStudent/')
		elif len(phone) != 10:
			messages.error(request, "Phone Number must be 10 digits")
			return redirect('/signupStudent/')
		elif phone.isdigit() == False:
			messages.error(request, "Phone Number must be numeric")
			return redirect('/signupStudent/')
		else:
			signupStudent = SignupStudent(
				username=username,
				firstName=firstName,
				studentCode=studentCode,
				lastName=lastName,
				email=email,
				password=password,
				phone=phone,
				location=location,
				latitude=latitude,
				longitude=longitude
			)
			signupStudent.save()
		return redirect('/loginStudent/')
	return render(request, 'tutor/signupStudent.html',{"school_list":school_list})

def addStudents(request):
	if request.method=="POST":
		print(request.POST)
		firstName = request.POST.get('firstName', '')
		lastName = request.POST.get('lastName', '')
		email = request.POST.get('email', '')
		username = email
		phone = request.POST.get('phone', '')
		password = phone
		count= SignupStudent.objects.all().count()
		count=count+1
		name= request.POST.get('firstName', '')
		ch1=str("%04d" % count)
		ch2=str(name[0:2])
		studentCode=ch2+ch1
		schoolName = request.POST.get('schoolName', '')

		location = request.POST.get('schoolName', '')
		lat = request.POST.get('cityLat', 1)
		lng = request.POST.get('cityLng', 1)

		if firstName.isalpha() == False | lastName.isalpha() == False | schoolName.isalpha() == False:
			messages.error(request, "Name must be alphabetical")
			return redirect('/addStudents/')
		if len(phone) != 10:
			messages.error(request, "Phone Number must be 10 digits")
			return redirect('/addStudents/')
		if SignupStudent.objects.filter(email=email).exists():
			messages.error(request, "Student with This Email Exists")
			return redirect('/addStudents/')
		if SignupStudent.objects.filter(phone=phone).exists():
			messages.error(request, "Phone Number is Already Registered")
			return redirect('/addStudents/')

		signupStudent = SignupStudent(
			username=username,
			firstName=firstName,
			studentCode=studentCode,
			lastName=lastName,
			email=email,
			password=password,
			phone=phone,
			schoolName=schoolName,
			location=location,
			latitude=lat,
			longitude=lng
		)
		school = School(name=schoolName)
		school.save()
		signupStudent.save()
		b = signupStudent
		cookieVAL = request.session.get('CoachingCentre',None)
		if(not cookieVAL):
			return HttpResponse("You are not logged in!")
		centre = SignupCoachingCentre.objects.get(s_no=cookieVAL)
		addSI = AddStudentInst(
				username=b.username,
				instituteName=centre.instituteName,
				instituteCode=centre.instituteCode,
				conector = b
			)
		addSI.save()

		ctn = request.POST.getlist('ctn_combined')
		cn = request.POST.getlist('cn_combined')
		ttn = request.POST.getlist('ttn_combined')
		ttn = [x.replace("\r","") for x in ttn]
		batchName = request.POST.getlist('batchN_combined')
		feeDis = request.POST.getlist('feedis_combined')
		asiObj = addSI
		for x in range(len(ttn)):
			try:
				temp = float(feeDis[x])
			except:
				try:
					temp = int(feeDis[x])
				except:
					temp = 0
			savTut = AddStudentDetail(
					username=asiObj,
					courseName = ctn[x] ,
					forclass = cn[x] ,
					teachType = ttn[x] ,
					batch = batchName[x],
					feeDisc = temp
				)
			savTut.save()
		return HttpResponse("""
				<script>
					alert('Student Added Sucessfully');
					window.location.href = "/addStudents";
				</script>
			""")


	schools = School.objects.all()
	school_list = list(map(str,schools))

	data = TeachingType.objects.values_list('courseName','forclass','teachType')
	processed_data = {}
	for x in data:
		processed_data[x[0]] = [x[1].split(", "),x[2].split("\n")]
	return render(
		request,
		'tutor/addStudents.html',
		{
			"data":TeachingType.objects.all(),
			"jsdata":dumps(processed_data),
			"school_list":school_list,
			'batch':BatchTiming.objects.all()
		}
	)

def addStudentInst(request,snum):
	b = SignupStudent.objects.get(snum=snum)
	cookieVAL = request.session.get('CoachingCentre',None)
	if(not cookieVAL):
		return HttpResponse("You are not logged in!")
	centre = SignupCoachingCentre.objects.get(s_no=cookieVAL)
	addSI = AddStudentInst(
			username=b.username,
			instituteName=centre.instituteName,
			instituteCode=centre.instituteCode,
			conector = b
		)
	addSI.save()
	return addStudentDetail(request,snum)
	# return redirect('/addStudentDetail/'+str(snum))


def addStudentDetail(request,sno):
	cookieVAL = request.session.get('CoachingCentre',None)
	if(not cookieVAL):
		return HttpResponse("You are not logged in!")
	centre = SignupCoachingCentre.objects.get(s_no=cookieVAL)
	batches = centre.BatchTiming.all()
	if(request.method=='POST'):
		print(request.POST)
		ctn = request.POST.getlist('ctn_combined')
		cn = request.POST.getlist('cn_combined')
		ttn = request.POST.getlist('ttn_combined')
		ttn = [x.replace("\r","") for x in ttn]
		batchName = request.POST.getlist('batchN_combined')
		feeDis = request.POST.getlist('feedis_combined')
		signUpObj = SignupStudent.objects.get(snum=sno)
		print(signUpObj.username,centre.instituteName)
		asiObj = AddStudentInst.objects.get(username=signUpObj.username, instituteName=centre.instituteName)
		cookieVAL = request.session.get('CoachingCentre')
		if(not cookieVAL):
			return HttpResponse("You are not logged in!")
		for x in range(len(ttn)):
			try:
				temp = float(feeDis[x])
			except:
				try:
					temp = int(feeDis[x])
				except:
					temp = 0
			savTut = AddStudentDetail(
					username=asiObj,
					courseName = ctn[x] ,
					forclass = cn[x] ,
					teachType = ttn[x] ,
					batch = batchName[x],
					feeDisc = temp
				)
			savTut.save()
		return redirect("/dashboard")
	data = TeachingType.objects.values_list('courseName','forclass','teachType')
	processed_data = {}
	for x in data:
		processed_data[x[0]] = [x[1].split(", "),x[2].split("\n")]
	return render(
		request,
		'tutor/addStudentInst.html',
		{
			"data":TeachingType.objects.all(),
			"jsdata":dumps(processed_data),
			"batches":batches
		}
	)


def searchUserStudent(request):
	if request.method=="POST":
		print(request.POST)
		# get logged in coaching center
		coachingCtr = request.session.get('CoachingCentre')
		# if coaching center is not logged in then redirecr
		if not coachingCtr:
			return HttpResponse("<script>alert('Coaching Center is not logged in');window.location.href = '/loginCoachingCentre';</script>")
		# data to be searched
		srch = request.POST.get('srh', '')
		if srch:
			match = SignupStudent.objects.filter(Q(username__icontains=srch))
			print('match',match)
			# currently signed in coaching center
			currentCC = SignupCoachingCentre.objects.get(s_no=coachingCtr)
			cleanedData = []
			# iterating over all matching queres
			for x in match:
				print('here',x)
				# iteration over all mathing enrollTutors objects
				for y in x.AddStudentInst.all():
					if(currentCC.instituteCode == y.instituteCode):
						break
				# if for any enrollTutors object corresponding
				# to SignupTutor object contains the institute
				# code for currently signed in institute then it
				# is not concidered
				else:
					cleanedData.append(x)
			print("cleaned", cleanedData)
			if len(match):
				return render(request,'tutor/searchUserStudent.html', {'sr':cleanedData})
			else:
				messages.error(request,'no result found')
		else:
			return HttpResponseRedirect('/searchUserStudent/')
	return render(request, 'tutor/searchUserStudent.html')

def viewStudents(request):
	# all student list
	cookieVAL = request.session.get('CoachingCentre')
	if(cookieVAL==None):
		return HttpResponse("<script>alert('Coaching Center is not logged in.')</script>")
	inst = SignupCoachingCentre.objects.get(s_no=cookieVAL)
	students = AddStudentInst.objects.filter(Q(instituteName=inst.instituteName))
	# sending variable
	params = {'students':students}
	return render(request, 'tutor/viewStudents.html', params)

def searchStudent(request):
	if request.method=="POST":
		srch = request.POST.get('srh', '')
		if srch:
			match = AddStudents.objects.filter(Q(studentName__icontains=srch) |
											  Q(courseName__icontains=srch) |
											  Q(feeStatus__icontains=srch)
											  )
			print(match)
			if match:
				return render(request,'tutor/searchStudent.html', {'sr':match})
			else:
				messages.error(request,'no result found')
		else:
			return HttpResponseRedirect('/searchStudent/')
	return render(request, 'tutor/searchStudent.html')

def deleteStudent(request,sno):
	try:
		# finding object to be deleted
		obj = AddStudentInst.objects.get(snum=sno)
		obj.delete()
	except Exception as e:
		# if object not found
		print(e)
	return redirect('/viewStudents')

def deleteArchiveStudent(request,sno):
	try:
		ArchiveStudents.objects.get(snum=sno).delete()
	except:
		print(sno)
	return redirect('/archiveStudentList')

def archiveStudent(request):
	if(request.method=='POST'):
		# try:
		# finding object list to be archived
		data = request.POST.getlist('ids')
		for sid in data:
			oldObj = AddStudentInst.objects.get(snum=sid)
			# exchanging data
			try:
				temp = oldObj.AddStudentDetail.all()[0]
			except:
				temp = AddStudentDetail()
				temp.save()
			newobj = ArchiveStudents(
				username=oldObj.username,
				conector=oldObj.conector,
				instituteName=oldObj.instituteName,
				instituteCode=oldObj.instituteCode,
				addStudentDetail = temp
			)
			newobj.save()
			oldObj.delete()
		return redirect('/viewStudents')
		# except Exception as e:
		# 	# if object not found
		# 	print('archiveStudent > ',e)
	return redirect('/viewStudents')

def removeFromArchiveStudent(request):
	if(request.method=='POST'):
		try:
			# finding object list to be archived
			data = request.POST.getlist('ids')
			for sid in data:
				oldObj = ArchiveStudents.objects.get(snum=sid)
				# exchanging data
				newobj = AddStudentInst(
					username=oldObj.username,
					conector=oldObj.conector,
					instituteName=oldObj.instituteName,
					instituteCode=oldObj.instituteCode
				)
				oldObj.delete()
				newobj.save()
			return redirect('/viewStudents')
		except Exception as e:
			# if object not found
			print(e)
	return redirect('/viewStudents')

def archiveStudentList(request):
	coachingCenterLoggedIn = request.session.get('CoachingCentre')
	print('cc',coachingCenterLoggedIn)
	# if cc is not logged in then redirecr
	if(not coachingCenterLoggedIn):
		return HttpResponse("<script>alert('Coaching Center is not logged in.');window.location.href = '/loginCoachingCentre/';</script>")
	# currently signed in student
	currentCC = SignupCoachingCentre.objects.get(s_no=coachingCenterLoggedIn)
	print(currentCC.instituteCode)
	data = ArchiveStudents.objects.all()
	# data = ArchiveStudents.objects.filter(instituteCode=currentCC.instituteCode)
	print(data)
	return render(request,'tutor/archiveStudentList.html',{'student':data})


def editStudent(request,sno):
	schools = School.objects.all()
	school_list = list(map(str,schools))
	data = TeachingType.objects.values_list('courseName','forclass','teachType')
	processed_data = {}
	for x in data:
		processed_data[x[0]] = [x[1].split(", "),x[2].split("\n")]
	qry = AddStudentInst.objects.get(snum=sno)
	jsonqry = [model_to_dict(x) for x in qry.AddStudentDetail.all()]
	jsonqry = json.dumps(jsonqry,cls=DjangoJSONEncoder)
	stname = qry.username
	stemail = qry.conector.email
	stphone = qry.conector.phone

	cookieVAL = request.session.get('CoachingCentre')
	if(cookieVAL==None):
		return HttpResponse("<script>alert('Coaching Center is not logged in.')</script>")
	inst = SignupCoachingCentre.objects.get(s_no=cookieVAL)
	courses = inst.AddCourses.all()

	params = {
		'stfname':qry.conector.firstName,
		'stlname':qry.conector.lastName,
		'stemail':stemail,
		'stphone':stphone,
		'courses':courses,
		'qry':qry,
		"data":TeachingType.objects.all(),
		"jsdata":dumps(processed_data),
		"school_list":school_list,
		'batch':BatchTiming.objects.all(),
		'jsonqry':jsonqry
		}
	if request.method=="POST":
		check1 = request.POST.getlist('check')
		check=', '.join(check1)
		radio = request.POST.getlist('radio')
		changeObj = AddStudentInst.objects.get(snum=sno).AddStudentDetail.all()[0]
		# changeObj(courseName=check,feeStatus=radio)
		return redirect("/viewStudents/")

	if request.method=="POST":
		print(request.POST)
		phone = request.POST.get('phone', '')
		schoolName = request.POST.get('schoolName', '')
		cookieVAL = request.session.get('CoachingCentre',None)
		if(not cookieVAL):
			return HttpResponse("You are not logged in!")

		centre = SignupCoachingCentre.objects.get(s_no=cookieVAL)
		addSI = AddStudentInst.objects.get(snum=sno)
		signupObj = addSI.conector
		signupObj.phone = phone
		signupObj.save()

		ctn = request.POST.getlist('ctn_combined')
		cn = request.POST.getlist('cn_combined')
		ttn = request.POST.getlist('ttn_combined')
		ttn = [x.replace("\r","") for x in ttn]
		batchName = request.POST.getlist('batchN_combined')
		feeDis = request.POST.getlist('feedis_combined')

		asiObj = addSI

		for x in assiObj.AddStudentDetail.all():
			print(x)
			# x.delete()

		for x in range(len(ttn)):
			try:
				temp = float(feeDis[x])
			except:
				try:
					temp = int(feeDis[x])
				except:
					temp = 0
			savTut = AddStudentDetail(
					username=asiObj,
					courseName = ctn[x] ,
					forclass = cn[x] ,
					teachType = ttn[x] ,
					batch = batchName[x],
					feeDisc = temp
				)
			savTut.save()
		return HttpResponse("""
				<script>
					alert('Student Added Sucessfully');
					window.location.href = "/addStudents";
				</script>
			""")
	return render(request, 'tutor/editStudent.html', params)

def addFeesC(request):
	courses = TeachingType.objects.all()
	params = {'courses':courses}
	if request.method=="POST":
		print(request.POST)
		forclass = request.POST.get('forclass')
		teachType = request.POST.get('teachType')
		if 'ajax_getinfo' in request.POST:
			courseName = request.POST.get('courseName')
			qry = TeachingType.objects.filter(Q(courseName__icontains=courseName))
			a = TeachingType.objects.filter(Q(courseName__icontains=courseName)).values('forclass','teachType','duration')
			b = list(a)
			c = b[0]["forclass"]
			t = b[0]["teachType"]
			d = b[0]["duration"]
			classes = list(c.split(', '))
			teachings = list(t.split('\n'))
			durations = list(d.split('\n'))
			param = {'classes':classes,'teachings':teachings,'durations':durations}
			return JsonResponse(param)
		else:
			print(request.POST)
			courseName = request.POST.get('courseName')
			course = AddCourses.objects.filter(Q(courseName__icontains=courseName))[0]
			forclass = request.POST.get('forclass')
			teachType = request.POST.get('check')
			duration = request.POST.get('duration')
			discValidity = request.POST.get('discValidity')
			discValidity = datetime.strptime(discValidity,'%Y-%m-%d')

			try:
				feeDisc = float(request.POST.get('feeDisc'))
				fee_amt = float(request.POST.get('feeamt'))
				tax = float(request.POST.get('tax'))
				final_amt = float(request.POST.get('final'))
				extraChargeType = int(request.POST.get('chargeType'))
				no_of_installment1 = request.POST.getlist('no_of_installment')
				no_of_installment=','.join(no_of_installment1)
				no_of_installment1 = [int(x) for x in no_of_installment1]
				extra_charge1 = request.POST.getlist('echarge')
				print(extra_charge1)
				extra_charge=','.join(extra_charge1)
				print(extra_charge)
				extra_charge1 = [float(x) for x in extra_charge1]
			except Exception as e:
				return HttpResponse(f"Wrong Data Type! - {e}")
			finalValue = 0
			if(extraChargeType):
				finalValue = final_amt + sum(extra_charge1)
			else:
				extra_charge1 = [((fee_amt*x)/100) for x in extra_charge1]
				feeCalc = fee_amt + sum(extra_charge1)
				finalValue = feeCalc + ((feeCalc*tax)/100)
			finalValue-=feeDisc
			addFees = AddFeesC(
					course= course,
					courseName = courseName,
					forclass = forclass,
					teachType = teachType,
					duration = duration,
					fee_amt = fee_amt,
					tax = tax,
					final_amt = final_amt,
					no_of_installment = no_of_installment,
					extra_charge = extra_charge,
					typeOfCharge = extraChargeType,
					final_amount = finalValue,
					discValidity= discValidity,
					feeDisc= feeDisc,
				)
			addFees.save()
	return render(request, 'tutor/addFees.html',params)

"""
Use addfeesC instead
"""
# def addFees(request):
# 	courses = AddCourses.objects.all()
# 	params = {'courses':courses}
# 	if request.method=="POST":
# 		courseName = request.POST.get('courseName')
# 		teachType1 = request.POST.getlist('check')
# 		teachType=', '.join(teachType1)
# 		duration = request.POST.get('duration', '')
# 		feeDuration1 = request.POST.getlist('fee_duration', '')
# 		feeDuration=', '.join(feeDuration1)
# 		no_of_installment = request.POST.get('no_of_installment', '')
# 		feeamt = request.POST.get('feeamt', '')
# 		a = AddCourses.objects.filter(Q(courseName__icontains=courseName)).values('courseName')
# 		print(a)
# 		if a:
# 			addFees = AddFees(courseName=courseName,teachType=teachType,duration=duration,feeDuration=feeDuration,no_of_installment=no_of_installment,feeamt=feeamt)
# 			addFees.save()
# 			return redirect("/viewFees/")
# 		else:
# 			messages.error(request, "Course Does not Exist.")
# 			return redirect('/addFees/')
# 	return render(request, 'tutor/addFees.html',params)

def viewFees(request):
	cookieVAL = request.session.get('CoachingCentre',None)
	if(not cookieVAL):
		return HttpResponse("You are not logged in!")
	centre = SignupCoachingCentre.objects.get(s_no=cookieVAL)
	courses = centre.AddCourses.all()
	fees = [course.AddFeesC.all() for course in courses]
	print(fees)

	fees = AddFeesC.objects.all()

	params = {'fees':fees,'centre':centre}
	return render(request, 'tutor/viewFees.html', params)

def archiveFees(request):
	if request.method=='POST':
		ids = request.POST.getlist('ids')
		for x in ids:
			oldOnj = AddFeesC.objects.get(sno=x)
			newObj = ArchiveFees(
				course = oldOnj.course,
				courseName = oldOnj.courseName,
				forclass = oldOnj.forclass,
				teachType = oldOnj.teachType,
				duration = oldOnj.duration,
				fee_amt = oldOnj.fee_amt,
				tax = oldOnj.tax,
				final_amt = oldOnj.final_amt,
				no_of_installment = oldOnj.no_of_installment,
				typeOfCharge = oldOnj.typeOfCharge,
				extra_charge = oldOnj.extra_charge,
				final_amount = oldOnj.final_amount,
				)
			newObj.save()
			oldOnj.delete()
	return redirect('/archiveFeeList')

def undoArchiveFees(request):
	if request.method=='POST':
		ids = request.POST.getlist('ids')
		for x in ids:
			oldOnj = ArchiveFees.objects.get(sno=x)
			newObj = AddFeesC(
				course = oldOnj.course,
				courseName = oldOnj.courseName,
				forclass = oldOnj.forclass,
				teachType = oldOnj.teachType,
				duration = oldOnj.duration,
				fee_amt = oldOnj.fee_amt,
				tax = oldOnj.tax,
				final_amt = oldOnj.final_amt,
				no_of_installment = oldOnj.no_of_installment,
				typeOfCharge = oldOnj.typeOfCharge,
				extra_charge = oldOnj.extra_charge,
				final_amount = oldOnj.final_amount,
				)
			newObj.save()
			oldOnj.delete()
	return redirect('/viewFees')

def deleteArchiveFee(request,sno):
	obj = ArchiveFees.objects.get(sno=sno)
	obj.delete()
	return redirect('/viewFees')

def searchFee(request):
	if request.method=="POST":
		cookieVAL = request.session.get('CoachingCentre',None)
		if(not cookieVAL):
			return HttpResponse("You are not logged in!")
		centre = SignupCoachingCentre.objects.get(s_no=cookieVAL)
		srch = request.POST.get('srh', '')
		if srch:
			match = AddFeesC.objects.filter(Q(teachType__icontains=srch) |
											  Q(courseName__icontains=srch) |
											  Q(duration__icontains=srch)
											  )
			print(match)
			if match:
				return render(request,'tutor/searchFee.html', {'sr':match})
			else:
				messages.error(request,'no result found')
		else:
			return HttpResponseRedirect('/searchFee/')
	return render(request, 'tutor/searchFee.html')

def deleteFee(request,sno):
	obj = AddFeesC.objects.get(sno=sno)
	obj.delete()
	return redirect('/viewFees')

def editFee(request,sno):
	# courses = AddCourses.objects.all()
	# params = {'courses':courses,}
	params = {}
	qry = AddFeesC.objects.get(sno=sno)
	params['qry'] = qry
	params['jsonqry'] = model_to_dict(qry)
	params['jsonqry'] = json.dumps(params['jsonqry'],cls=DjangoJSONEncoder)
	courses = TeachingType.objects.all()
	params['courses']=courses
	print(params)

	if request.method=="POST":
		if 'ajax_getinfo' in request.POST:
			courseName = request.POST.get('courseName')
			qry = TeachingType.objects.filter(Q(courseName__icontains=courseName))
			a = TeachingType.objects.filter(Q(courseName__icontains=courseName)).values('forclass','teachType','duration')
			b = list(a)
			c = b[0]["forclass"]
			t = b[0]["teachType"]
			d = b[0]["duration"]
			classes = list(c.split(', '))
			teachings = list(t.split('\n'))
			durations = list(d.split('\n'))
			param = {'classes':classes,'teachings':teachings,'durations':durations}
			return JsonResponse(param)
		else:
			print(request.POST)
			courseName = request.POST.get('courseName')
			forclass = request.POST.get('forclass')
			teachType = request.POST.get('check')
			duration = request.POST.get('duration')
			discValidity = request.POST.get('validity')
			discValidity = datetime.strptime(discValidity,'%Y-%m-%d')

			try:
				feeDisc = float(request.POST.get('discount'))
				fee_amt = float(request.POST.get('feeamt'))
				tax = float(request.POST.get('tax'))
				final_amt = float(request.POST.get('final'))
				extraChargeType = int(request.POST.get('chargeType'))
				no_of_installment1 = request.POST.getlist('no_of_installment')
				no_of_installment=','.join(no_of_installment1)
				no_of_installment1 = [int(x) for x in no_of_installment1]
				extra_charge1 = request.POST.getlist('echarge')
				extra_charge=','.join(extra_charge1)
				extra_charge1 = [float(x) for x in extra_charge1]
			except Exception as e:
				return HttpResponse(f"Wrong Data Type! - {e}")
			finalValue = 0
			if(extraChargeType):
				finalValue = final_amt + sum(extra_charge1)
			else:
				extra_charge1 = [((fee_amt*x)/100) for x in extra_charge1]
				feeCalc = fee_amt + sum(extra_charge1)
				finalValue = feeCalc + ((feeCalc*tax)/100)
			finalValue-=feeDisc
			AddFeesC.objects.filter(sno=sno).update(
					courseName = courseName,
					forclass = forclass,
					teachType = teachType,
					duration = duration,
					fee_amt = fee_amt,
					tax = tax,
					final_amt = final_amt,
					no_of_installment = no_of_installment,
					extra_charge = extra_charge,
					typeOfCharge = extraChargeType,
					final_amount = finalValue,
					discValidity= discValidity,
					feeDisc= feeDisc,
				)
			return redirect("/viewFees/")
	return render(request, 'tutor/editFee.html', params)

def archiveFeeList(request):
	fee = ArchiveFees.objects.all()
	params = {'fee':fee}
	return render(request, 'tutor/archiveFeeList.html', params)

def submitFee(request):
	if request.method == 'POST':
		print(request.POST)
		cookieVAL = request.session.get('CoachingCentre',None)
		if(not cookieVAL):
			return HttpResponse("You are not logged in!")
		centre = SignupCoachingCentre.objects.get(s_no=cookieVAL)
		userAction = request.POST.get("userAction",None)

		if(userAction=='studentSearch'):
			name = request.POST.get("userName")
			data = AddStudentInst.objects.filter((
					Q(conector__username__contains=name) |
					Q(conector__firstName__contains=name) |
					Q(conector__lastName__contains=name) |
					Q(conector__email__contains=name)) &
					Q(instituteName=centre.instituteName)
				)
			print(data)
			return render(request, 'tutor/submitFee.html', {'userData':data})

		elif(userAction=='subjectSearch'):
			userId = request.POST.get('userId')
			user = AddStudentInst.objects.get(snum=userId)
			data = user.AddStudentDetail.all()
			print("Subject Search",data,user)
			return render(request, 'tutor/submitFee.html', {'subjectData':data,'username':user})

		elif(userAction=='studentFee'):
			subjectId = request.POST.get('subjectId')
			dataObj = AddStudentDetail.objects.get(snum=subjectId)
			print(dataObj.instalment)
			addFeeObj = AddFeesC.objects.filter(
					courseName  = dataObj.courseName,
					forclass    = dataObj.forclass,
					teachType   = dataObj.teachType
				)
			print(addFeeObj)
			if(addFeeObj):
				addFeeObj = addFeeObj[0]
			else:
				return HttpResponse(f"Fees for this subject Combination doesnot Exist! <br>courseName  = {dataObj.courseName},<br>forclass = {dataObj.forclass},<br>teachType = {dataObj.teachType}")
			feeObj = dataObj.fees.all()
			print(feeObj)
			if(not feeObj):
				feeObjNew = SubmitFees(
						username        = dataObj,
						subject         = addFeeObj.courseName,
						totalFee        = addFeeObj.final_amount,
						balanceFee      = addFeeObj.final_amount,
						totalInstallments=dataObj.instalment,
						instalmentDue   = dataObj.instalment
					)
				print("bs",feeObjNew.instalmentDue)
				feeObjNew.save()
				feeObj = dataObj.fees.all()

			feeObj = feeObj[0]
			print(feeObj.instalmentDue)
			try:
				payment = feeObj.balanceFee/feeObj.instalmentDue
			except:
				payment = feeObj.balanceFee
			print(payment)
			inputData = {
				'installmentNumber' : feeObj.totalInstallments - feeObj.instalmentDue + 1,
				'payment' : payment,
				'feeId' : feeObj.sno,
			}
			installmentnotcomplete = (feeObj.instalmentDue!=0)
			return render(
				request,
				'tutor/submitFee.html',
				{
					'inputData':inputData,'installmentsDone':feeObj.totalInstallments - feeObj.instalmentDue, 'feeObj':feeObj,'installmentnotcomplete':installmentnotcomplete
				}
			)
		elif(userAction=='submitFee'):
			iNum = int(float(request.POST.get('iNum')))
			fees = float(request.POST.get('fees'))
			payed = float(request.POST.get('payed'))
			feeId = int(float(request.POST.get('feeId')))
			submitObj = SubmitFees.objects.get(sno=feeId)
			print(dir(submitObj.feePayed))
			print(submitObj.feePayed.to_integral_value())
			submitObj.feePayed = F('feePayed') + payed
			submitObj.balanceFee = F('balanceFee') - payed
			submitObj.instalmentDue = F('instalmentDue') - 1
			submitObj.save()
			newInstallment = Instalment(
					feeObj          = submitObj,
					instalmentNum   = iNum,
					paymentExp      = fees,
					paymentDone     = payed
				)
			newInstallment.save()

	return render(request, 'tutor/submitFee.html')

def enrolledTutorsObjectToDict(obj):
	data = {
		'tutorCode':obj.tutorCode,
		'username':obj.username,
		'firstName':obj.firstName,
		'lastName':obj.lastName,
		'email':obj.email,
		'distance':float(obj.distance),
		'phone':obj.phone,
	}
	if(obj.signupTutorContinued.all()):
		obj = obj.signupTutorContinued.all()[0]
		data['availability'] = obj.availability
		data['qualification'] = obj.qualification
		data['experience'] = float(obj.experience)
		data['description'] = obj.description
		data['gender'] = obj.gender
		data['courseName'] = obj.courseName
		data['forclass'] = obj.forclass
		data['fees'] = float(obj.fees)
		data['avatar'] = float(obj.avatar)
		try:
			data['photo'] = obj.photo.url
		except:
			data['photo'] = None
	print(data)
	return data

def enrolledTutors(request):
	jsonLocalData = loads(open('cc.txt','r').read())
	if(request.method=='POST'):
		searchQuery = Q(budget__gte=-1000)
		className = request.POST.get('className')
		courceName = request.POST.get('courseName')
		budgetVal = request.POST.get('budget')
		la1 = float(request.POST.get('cityLat'))
		lo1 = float(request.POST.get('cityLng'))
		if(courceName):
			searchQuery &= Q(courseName=courceName)
		if(className):
			searchQuery &= Q(forclass=className)
		if(budgetVal):
			searchQuery &= Q(budget__lte=budgetVal)
		allData = SignupTutor.objects.filter(searchQuery)
		finalData = []
		for x in allData:
			la2 = float(x.connector.latitude)
			lo2 = float(x.connector.longitude)
			distance = distanceBwAB((la1,lo1),(la2,lo2)).km
			if(float(tutorObj.distance)<=float(distance)):
				finalData.append(x)
		jsonData = []
		for x in finalData:
			jsonData.append(enrolledTutorsObjectToDict(x))
		return render(request, "tutor/enrolledTutors.html",{'allData':finalData,'jsonData':jsonData,'jsonLocalData':jsonLocalData})
	allData = SignupTutor.objects.all()
	jsonData = []
	for x in allData:
		jsonData.append(enrolledTutorsObjectToDict(x))
	print(jsonData)
	jsonData = dumps(jsonData)
	return render(request, "tutor/enrolledTutors.html",{'allData':allData,'jsonData':jsonData,'jsonLocalData':jsonLocalData})

def postTution(request):
	if(request.method=='POST'):
		print(request.POST)
		studentLoggedin = request.session.get('Student')
		# if student is not logged in then redirect
		if not studentLoggedin:
			return HttpResponse("<script>alert('Student is not logged in');window.location.href = '/loginStudent';</script>")
		# currently signed in student
		currentS = SignupStudent.objects.get(snum=studentLoggedin)
		# saving data
		postTutionObj = PostTution(
				connector = currentS,
				courseName = request.POST.get('ctn'),
				forclass = request.POST.get('cn'),
				teachingMode = request.POST.get('tm'),
				genderPreference = request.POST.get('gp'),
				whenToStart = request.POST.get('sd'),
				description = request.POST.get('description'),
				budget = request.POST.get('budget'),
				budgetVal = request.POST.get('budgetvalue',0),
				numberOfSessions =request.POST.get('monthlydigit',0)
			)
		postTutionObj.save()
		# redirect on sucessful save
		return redirect('/dashboardStudent')
	data = TeachingType.objects.values_list('courseName','forclass','teachType')
	processed_data = {}
	for x in data:
		processed_data[x[0]] = [x[1].split(", "),x[2].split("\n")]
	return render(
		request,
		'tutor/postTution.html',
		{
			"data":TeachingType.objects.all(),
			"jsdata":dumps(processed_data)
		}
	)

def viewTution(request):
	if(request.method=='POST'):
		# deletion
		delteSno = request.POST.get('delteSno')
		try:
			PostTution.objects.get(sno = delteSno).delete()
		except Exception as e:
			print(e)
		return redirect('/viewTution/')
	studentLoggedin = request.session.get('Student')
	# if student center is not logged in then redirecr
	if not studentLoggedin:
		return HttpResponse("<script>alert('Student is not logged in');window.location.href = '/loginStudent';</script>")
	# currently signed in student
	currentS = SignupStudent.objects.get(snum=studentLoggedin)
	return render(request, 'tutor/viewTution.html', {'data':currentS})

def editTution(request,sno):
	return render(request, 'tutor/editTution.html')

def postAssignment(request):
	if(request.method=='POST'):
		studentLoggedin = request.session.get('Student')
		# if coaching center is not logged in then redirecr
		if not studentLoggedin:
			return HttpResponse("<script>alert('Student is not logged in');window.location.href = '/loginStudent';</script>")
		# currently signed in student
		currentS = SignupStudent.objects.get(snum=studentLoggedin)
		# saving data
		postAssigObj = PostAssignment(
				connector = currentS,
				courseName = request.POST.get('ctn'),
				forclass = request.POST.get('cn'),
				description = request.POST.get('description'),
				descriptionFile = request.FILES.get('file'),
				requirement = request.POST.get('requirement'),
				budget = request.POST.get('budget'),
			)
		postAssigObj.save()
		# redirect on sucessful save
		return redirect('/dashboardStudent')
	data = TeachingType.objects.values_list('courseName','forclass','teachType')
	processed_data = {}
	for x in data:
		processed_data[x[0]] = [x[1].split(", "),x[2].split("\n")]
	return render(
		request,
		'tutor/postAssignment.html',
		{
			"data":TeachingType.objects.all(),
			"jsdata":dumps(processed_data)
		}
	)

def viewAssignment(request):
	if(request.method=='POST'):
		# deletion
		delteSno = request.POST.get('delteSno')
		try:
			PostAssignment.objects.get(sno = delteSno).delete()
		except Exception as e:
			print(e)
		return redirect('/viewAssignment/')
	studentLoggedin = request.session.get('Student')
	# if student is not logged in then redirecr
	if not studentLoggedin:
		return HttpResponse("<script>alert('Student is not logged in');window.location.href = '/loginStudent';</script>")
	# currently signed in student
	currentS = SignupStudent.objects.get(snum=studentLoggedin)
	return render(request, 'tutor/viewAssignment.html', {'data':currentS})

def editAssignment(request,sno):
	return render(request, 'tutor/editAssignment.html')

def enrolledInstututesTutor(request):
	TutorLoggedin = request.session.get('Tutor')
	print(TutorLoggedin)
	# if tutor is not logged in then redirecr
	if not TutorLoggedin:
		return HttpResponse("<script>alert('Tutor is not logged in');window.location.href = '/loginTutor/';</script>")
	# currently signed in tutor
	currentS = SignupTutor.objects.get(sno=TutorLoggedin)
	# enrolled institutes
	data = currentS.enrollTutors.all()
	print(data[0].AddTutorsInst.all()[0].teachType)
	return render(request,'tutor/enrolledInstututesTutor.html',{'data':data})

def enrolledInstututesStudent(request):
	studentLoggedin = request.session.get('Student')
	print(studentLoggedin)
	# if student is not logged in then redirecr
	if not studentLoggedin:
		return HttpResponse("<script>alert('Student is not logged in');window.location.href = '/loginStudent';</script>")
	# currently signed in student
	currentS = SignupStudent.objects.get(snum=studentLoggedin)
	# enrolled institutes
	data = currentS.AddStudentInst.all()
	return render(request,'tutor/enrolledInstututesStudent.html',{'data':data})

def ampm(inpTime):
	print(inpTime)
	# converting 24 hour time to 12 hour time
	temp = inpTime.split(":")
	hour = int(temp[0])
	minute = temp[1]
	if(hour==0):
		hour=12
		ending='AM'
	elif(hour==12):
		ending='PM'
	elif(hour>12):
		hour = str(hour%12).zfill(2)
		ending = 'PM'
	else:
		ending = 'AM'
	result = str(hour)+":"+str(minute)+":"+ending
	return result

def batchTiming(request):
	if(request.method=='POST'):
		#checking login
		cookieVAL = request.session.get('CoachingCentre')
		if(cookieVAL==None):
			return HttpResponse("<script>alert('Coaching Center is not logged in.')</script>")
		print(request.POST)
		if('delteSno' in request.POST):
			delObj = BatchTiming.objects.get(sno=request.POST.get('delteSno'))
			delObj.delete()
		else:
			#cleaning data
			batchName = request.POST.get('batchName')
			startTime = request.POST.get('startTime')
			endTime = request.POST.get('endTime')
			original = startTime+","+endTime
			# converting 24 hour time to 12 hour time
			try:
				startTime = ampm(startTime)
				endTime = ampm(endTime)
			except Exception as e:
				print(e)
			days = request.POST.getlist('forday')
			days = ", ".join(days)
			coachingCenter = SignupCoachingCentre.objects.get(s_no=cookieVAL)
			batchObj = BatchTiming(
					batchName = batchName,
					startTime = startTime,
					endTime   = endTime,
					coachingCenter = coachingCenter,
					days=days,
					original24time=original
				)
			batchObj.save()
	#checking login
	cookieVAL = request.session.get('CoachingCentre')
	if(cookieVAL==None):
		return HttpResponse("<script>alert('Coaching Center is not logged in.')</script>")
	coachingCenter = SignupCoachingCentre.objects.get(s_no=cookieVAL).BatchTiming.all()
	return render(request,'tutor/batchTiming.html',{'data':coachingCenter})

def batchTimingEdit(request,sno):
	if(request.method=='POST'):
		#checking login
		cookieVAL = request.session.get('CoachingCentre')
		if(cookieVAL==None):
			return HttpResponse("<script>alert('Coaching Center is not logged in.')</script>")
		#cleaning data
		batchName = request.POST.get('batchName')
		startTime = request.POST.get('startTime')
		endTime = request.POST.get('endTime')
		original = startTime+","+endTime
		# converting 24 hour time to 12 hour time
		try:
			startTime = ampm(startTime)
			endTime = ampm(endTime)
		except Exception as e:
			print(e)
		days = request.POST.getlist('forday')
		days = ", ".join(days)
		coachingCenter = SignupCoachingCentre.objects.get(s_no=cookieVAL)
		batchObj = BatchTiming.objects.get(sno=sno)
		batchObj.batchName = batchName
		batchObj.startTime = startTime
		batchObj.endTime = endTime
		batchObj.days = days
		batchObj.original24time = original
		batchObj.save()
		return redirect("/batchTiming")
	# determining preill data
	prefilObj = BatchTiming.objects.get(sno=sno)
	return render(request,'tutor/batchTimingEdit.html',{'prefilObj':prefilObj})

def tutorCalendar(request):
	return render(request,"tutor/tutorCalendar.html",{})

def profileCoachingCentre(request):
	schools = School.objects.all()
	school_list = list(map(str,schools))
	coachingCenterLoggedIn = request.session.get('CoachingCentre')
	print('cc',coachingCenterLoggedIn)
	# if cc is not logged in then redirecr
	if(not coachingCenterLoggedIn):
		return HttpResponse("<script>alert('Coaching Center is not logged in.');window.location.href = '/loginCoachingCentre/';</script>")
	# currently signed in student
	currentCC = SignupCoachingCentre.objects.get(s_no=coachingCenterLoggedIn)
	if(request.method=='POST'):
		if 'otpReceived' in request.POST:
			otp = request.POST.get('otp')
			email = request.POST.get('email')
			otp_obj = OTP.obects.get(type='any',user=email)
			if (currentCC.email==email) and otp_obj:
				if otp_obj.otp==otp:
					currentCC.emailValidated = True
					currentCC.save()
			otp_obj.delete()
			return redirect('/profileTutor/')
		else:
			print(request.POST)
			instName = request.POST.get('instituteName')
			phone = request.POST.get('phone')
			oldPassword = request.POST.get('oldPassword')
			newPassword = request.POST.get('newPassword')
			confPassword = request.POST.get('confirmPassword')
			latitude = request.POST.get('cityLat')
			longitude = request.POST.get('cityLng')
			loaction = request.POST.get('loc')
			image = request.POST.get('photo')
			showFees = request.POST.get('showFees')
			print('image',image)
			# avatar = request.POST.get('avatar',0)
			error = 0
			if(not phone.isdigit()):
				messages.error(request, "Phone number should be numeric.")
				error=1
			if(len(phone)!=10):
				messages.error(request, "Phone number should be 10 digits long.")
				error=1
			if(len(newPassword)<3 or len(newPassword)>20):
				messages.error(request, "Password length should be between 3 and 20")
				error=1
			if(oldPassword!=currentCC.password):
				messages.error(request,"Enter you correct old password.")
				error=1
			if(newPassword!=confPassword):
				messages.error(request,"New Password and Confirm Password donot match")
				error=1
			if(error==0):
				currentCC.instituteName = instName
				currentCC.password = newPassword
				currentCC.phone = phone
				currentCC.location = loaction
				currentCC.latitude = latitude
				currentCC.longitude = longitude
				currentCC.showFees = showFees

				if(image):
					if(image.isdigit()):
						currentCC.avatar = image
						currentCC.photo = None
					else:
						f,img = image.split(';base64,')
						ext = f.split('/')[-1]
						image = ContentFile(base64.b64decode(img),name='temp.'+ext)
						currentCC.avatar = 0
						currentCC.photo = image
				currentCC.save()
				currentCC = SignupCoachingCentre.objects.get(s_no=coachingCenterLoggedIn)
	responce = render(request,"tutor/profileCoachingCentre.html",{'centre':currentCC,'schools':schools})
	responce.set_cookie('CoachingCentreAvatar',currentCC.avatar)
	responce.set_cookie('CoachingCentrePhoto',currentCC.photo)
	return responce

def profileStudent(request):
	schools = School.objects.all()
	school_list = list(map(str,schools))
	studentLoggedin = request.session.get('Student')
	# if student is not logged in then rediret
	if(not studentLoggedin):
		return HttpResponse("<script>alert('Studnt Center is not logged in.');window.location.href = '/loginStudent/';</script>")
	# currently signed in student
	studentObj = SignupStudent.objects.get(snum=studentLoggedin)
	if(request.method=='POST'):
		if 'otpReceived' in request.POST:
			otp = request.POST.get('otp')
			email = request.POST.get('email')
			otp_obj = OTP.obects.get(type='any',user=email)
			if (studentObj.email==email) and otp_obj:
				if otp_obj.otp==otp:
					studentObj.emailValidated = True
					studentObj.save()
			otp_obj.delete()
			return redirect('/profileStudent/')
		else:
			print(request.POST)
			# assigning new values
			firstName = request.POST.get('firstName')
			lastName = request.POST.get('lastName')
			phone = request.POST.get('phone')
			oldPassword = request.POST.get('oldPassword')
			newPassword = request.POST.get('newPassword')
			confPassword = request.POST.get('confirmPassword')
			location = request.POST.get('loc')
			image = request.POST.get('photo')
			latitude = request.POST.get('cityLat')
			longitude = request.POST.get('cityLng')
			schoolName = request.POST.get('schoolName',"")
			# errors
			error = 0
			if(not phone.isdigit()):
				messages.error(request, "Phone number should be numeric.")
				error=1
			if(len(phone)!=10):
				messages.error(request, "Phone number should be 10 digits long.")
				error=1
			if(len(newPassword)<3 or len(newPassword)>20):
				messages.error(request, "Password length should be between 3 and 20")
				error=1
			if(oldPassword!=studentObj.password):
				messages.error(request,"Enter you correct old password.")
				error=1
			if(newPassword!=confPassword):
				messages.error(request,"New Password and Confirm Password donot match")
				error=1
			if(error==0):
				# saving new data
				studentObj.firstName = firstName
				studentObj.lastName = lastName
				studentObj.password = newPassword
				studentObj.phone = phone
				studentObj.location = location
				studentObj.schoolName = schoolName
				studentObj.latitude = latitude
				studentObj.longitude = longitude
				if(image):
					if(image.isdigit()):
						studentObj.avatar = image
						studentObj.photo = None
					else:
						f,img = image.split(';base64,')
						ext = f.split('/')[-1]
						image = ContentFile(base64.b64decode(img),name='temp.'+ext)
						studentObj.avatar = 0
						studentObj.photo = image
				studentObj.save()
				# new object
				studentObj = SignupStudent.objects.get(snum=studentLoggedin)


	responce = render(request,"tutor/profileStudent.html",{'student':studentObj,'school_list':school_list})
	responce.set_cookie('StudentAvatar',studentObj.avatar)
	responce.set_cookie('StudentPhoto',studentObj.photo)
	return responce

def profileTutor(request):
	schools = School.objects.all()
	school_list = list(map(str,schools))
	tutorLoggedIn = request.session.get('Tutor')
	print(tutorLoggedIn)
	# if tutor is not logged in then redirect
	if(not tutorLoggedIn):
		return HttpResponse("<script>alert('Tutor is not logged in.');window.location.href = '/loginTutor/';</script>")
	# currently signed in tutor
	tutorObj = SignupTutor.objects.get(sno=tutorLoggedIn)
	l = len(tutorObj.signupTutorContinued.all())
	try:
		signupTutContObj = tutorObj.signupTutorContinued.all()[l-1]
	except Exception as e:
		print(e)
	if(request.method=='POST'):

		if 'otpReceived' in request.POST:
			otp = request.POST.get('otp')
			email = request.POST.get('email')
			otp_obj = OTP.obects.get(type='any',user=email)
			if (tutorObj.email==email) and otp_obj:
				if otp_obj.otp==otp:
					tutorObj.emailValidated = True
					tutorObj.save()
			otp_obj.delete()
			return redirect('/profileTutor/')

		else:
			print(request.POST)
			# assigning new values
			firstName = request.POST.get('firstName')
			lastName = request.POST.get('lastName')
			phone = request.POST.get('phone')
			oldPassword = request.POST.get('oldPassword')
			newPassword = request.POST.get('newPassword')
			confPassword = request.POST.get('confirmPassword')
			location = request.POST.get('loc')
			availability = ', '.join(request.POST.getlist('availability'))
			qualification = request.POST.get('qualification')
			experience = request.POST.get('experience')
			description = request.POST.get('description')
			freeDemo = request.POST.get('fda')
			image = request.POST.get('photo')
			distance = request.POST.get('distance',0)
			gender = request.POST.get('gender','A')
			# courseName = request.POST.get('courseName')
			# forclass = request.POST.get('forclass')
			fees  = request.POST.get('fees',0)
			latitude = request.POST.get('cityLat')
			longitude = request.POST.get('cityLng')

			# errors
			error = 0
			if(not phone.isdigit()):
				messages.error(request, "Phone number should be numeric.")
				error=1
			if(len(phone)!=10):
				messages.error(request, "Phone number should be 10 digits long.")
				error=1
			if(len(newPassword)<3 or len(newPassword)>20):
				messages.error(request, "Password length should be between 3 and 20")
				error=1
			if(oldPassword!=tutorObj.password):
				messages.error(request,"Enter you correct old password.")
				error=1
			if(newPassword!=confPassword):
				messages.error(request,"New Password and Confirm Password donot match")
				error=1

			if(error==0):
				# saving new data
				tutorObj.firstName  = firstName
				tutorObj.lastName  = lastName
				tutorObj.password  = newPassword
				tutorObj.distance  = distance
				tutorObj.location  = location
				tutorObj.latitude  = latitude
				tutorObj.longitude  = longitude
				tutorObj.phone  = phone
				if(len(tutorObj.signupTutorContinued.all())):
					signupTutContObj = tutorObj.signupTutorContinued.all()[l-1]
					signupTutContObj.availability = availability
					signupTutContObj.qualification = qualification
					signupTutContObj.experience = experience
					signupTutContObj.description = description
					signupTutContObj.gender = gender
					# signupTutContObj.courseName = courseName
					# signupTutContObj.forclass = forclass
					signupTutContObj.fees = fees
					signupTutContObj.freeDemo = freeDemo
					if(image):
						if(image.isdigit()):
							print('asdd',image)
							signupTutContObj.avatar = image
							signupTutContObj.photo = None
						else:
							f,img = image.split(';base64,')
							ext = f.split('/')[-1]
							image = ContentFile(base64.b64decode(img),name='temp.'+ext)
							signupTutContObj.avatar = 0
							signupTutContObj.photo = image
					signupTutContObj.save()
				tutorObj.save()
				# new object
				tutorObj = SignupTutor.objects.get(sno=tutorLoggedIn)

	responce = render(request,"tutor/profileTutor.html",{'tutor':tutorObj,'schools':schools})
	responce.set_cookie('TutorAvatar',signupTutContObj.avatar)
	responce.set_cookie('TutorPhoto',signupTutContObj.photo)
	return responce


def viewAssignmentTutor(request):
	tutorLoggedIn = request.session.get('Tutor')
	print(tutorLoggedIn)
	# if tutor is not logged in then redirect
	if(not tutorLoggedIn):
		return HttpResponse("<script>alert('Tutor is not logged in.');window.location.href = '/loginTutor/';</script>")
	# currently signed in tutor
	tutorObj = SignupTutor.objects.get(sno=tutorLoggedIn)
	if(len(tutorObj.signupTutorContinued.all())==0):
		return HttpResponse("<script>alert('Tutor is not logged in.');window.location.href = '/loginTutor/';</script>")
	print(tutorObj.signupTutorContinued.all())
	tutorContiObj = tutorObj.signupTutorContinued.all()[0]
	classNames = tutorContiObj.forclass
	classNameList = []
	for x in classNames.split(';'):
		for y in x.split(', '):
			classNameList.append(y)
	courceNames = tutorContiObj.courseName
	courceNameList = []
	for x in courceNames.split(';'):
		for y in x.split(', '):
			courceNameList.append(y)

	currentS = PostAssignment.objects.all()
	print(currentS)
	# print(classNameList)
	# print(PostAssignment.objects.values('forclass'))
	initialQuery = Q(budget__gte=-1000)
	initialQuery &= Q(courseName__in=courceNameList)
	initialQuery &= Q(forclass__in=classNameList)
	initialQuery &= Q(budget__lte=tutorContiObj.fees)
	initialData = PostAssignment.objects.filter(initialQuery)
	la1 = float(tutorObj.latitude)
	lo1 = float(tutorObj.longitude)
	finalData = []
	for x in initialData:
		la2 = float(x.connector.latitude)
		lo2 = float(x.connector.longitude)
		distance = (((la1-la2)**2) + (lo1-lo2)**2)**0.5
		if(float(tutorObj.distance)<=float(distance)):
			finalData.append(x)
	print('res',initialData)
	if(request.method=='POST'):
		searchQuery = Q(budget__gte=-1000)
		className = request.POST.get('className')
		courceName = request.POST.get('courseName')
		budgetVal = request.POST.get('budget')
		la1 = float(request.POST.get('cityLat'))
		lo1 = float(request.POST.get('cityLng'))
		if(courceName):
			searchQuery &= Q(courseName=courceName)
		if(className):
			searchQuery &= Q(forclass=className)
		if(budgetVal):
			searchQuery &= Q(budget__lte=budgetVal)
		initialData = PostAssignment.objects.filter(searchQuery)
		finalData = []
		for x in initialData:
			la2 = float(x.connector.latitude)
			lo2 = float(x.connector.longitude)
			distance = distanceBwAB((la1,lo1),(la2,lo2)).km
			if(float(tutorObj.distance)<=float(distance)):
				finalData.append(x)
	jsonLocalData = loads(open('cc.txt','r').read())
	return render(request, "tutor/viewAssignmentTutor.html",{'allData':finalData,'jsonLocalData':jsonLocalData})

def enrolledStudents(request):
	# allData = PostTution.objects.all()
	# return render(request, "tutor/enrolledStudents.html",{'allData':allData})

	tutorLoggedIn = request.session.get('Tutor')
	print(tutorLoggedIn)
	# if tutor is not logged in then redirect
	if(not tutorLoggedIn):
		return HttpResponse("<script>alert('Tutor is not logged in.');window.location.href = '/loginTutor/';</script>")
	# currently signed in tutor
	tutorObj = SignupTutor.objects.get(sno=tutorLoggedIn)
	if(len(tutorObj.signupTutorContinued.all())==0):
		return HttpResponse("<script>alert('Tutor is not logged in.');window.location.href = '/loginTutor/';</script>")
	print(tutorObj.signupTutorContinued.all())
	tutorContiObj = tutorObj.signupTutorContinued.all()[0]
	classNames = tutorContiObj.forclass
	classNameList = []
	for x in classNames.split(';'):
		for y in x.split(', '):
			classNameList.append(y)
	courceNames = tutorContiObj.courseName
	courceNameList = []
	for x in courceNames.split(';'):
		for y in x.split(', '):
			courceNameList.append(y)

	currentS = PostAssignment.objects.all()
	print(currentS)
	# print(classNameList)
	# print(PostAssignment.objects.values('forclass'))
	initialQuery = Q(budget__gte=-1000)
	initialQuery &= Q(courseName__in=courceNameList)
	initialQuery &= Q(forclass__in=classNameList)
	initialQuery &= Q(budget__lte=tutorContiObj.fees)
	initialData = PostTution.objects.filter(initialQuery)
	try:
		la1 = float(tutorObj.latitude)
	except Exception as e:
		print(la1,2176,e)
		la1=1
	try:
		lo1 = float(tutorObj.longitude)
	except Exception as e:
		print(lo1,2181,e)
		lo1=1
	print('initialData',initialData)
	finalData = []
	for x in initialData:
		la2 = float(x.connector.latitude)
		lo2 = float(x.connector.longitude)
		distance = distanceBwAB((la1,lo1),(la2,lo2)).km
		print(distance)
		if(float(tutorObj.distance)<=float(distance)):
			finalData.append(x)
	print('res',finalData)
	if(request.method=='POST'):
		searchQuery = Q(budget__gte=-1000)
		className = request.POST.get('className')
		courceName = request.POST.get('courseName')
		budgetVal = request.POST.get('budget')
		la1 = float(request.POST.get('cityLat'))
		lo1 = float(request.POST.get('cityLng'))
		if(courceName):
			searchQuery &= Q(courseName=courceName)
		if(className):
			searchQuery &= Q(forclass=className)
		if(budgetVal):
			searchQuery &= Q(budget__lte=budgetVal)
		initialData = PostTution.objects.filter(searchQuery)
		finalData = []
		for x in initialData:
			la2 = float(x.connector.latitude)
			lo2 = float(x.connector.longitude)
			distance = distanceBwAB((la1,lo1),(la2,lo2)).km
			if(float(tutorObj.distance)<=float(distance)):
				finalData.append(x)
	jsonLocalData = loads(open('cc.txt','r').read())
	return render(request, "tutor/enrolledStudents.html",{'allData':finalData,'jsonLocalData':jsonLocalData})

@csrf_exempt
def ajaxLocation(request):
	if(request.method=='POST'):
		latitude = request.POST.get('cityLat')
		longitude = request.POST.get('cityLng')
		error = 0
		try:
			latitude = float(latitude)
		except:
			error = 1
		try:
			longitude = float(longitude)
		except:
			error = 1

		if(not error):
			location = str(geolocator.reverse(f"{latitude}, {longitude}").address)
			result = {'status':'success','result':location}
			return JsonResponse(result)
	result = {'status':'failed','result':(str(request.POST.get('cityLat')),str(request.POST.get('cityLng')))}
	return JsonResponse(result)


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

def makeAppointment(request):
	studentLoggedin = request.session.get('Student')
	# if student is not logged in then rediret
	if(not studentLoggedin):
		return HttpResponse("<script>alert('Student is not logged in.');window.location.href = '/loginStudent/';</script>")
	# currently signed in student
	studentObj = SignupStudent.objects.get(snum=studentLoggedin)
	print(studentLoggedin)
	if request.method=='POST':
		print(request.POST)
		# errors list
		errors = []

		# input date
		date = request.POST.get('date')
		try:
			# date conversion
			date = datetime.strptime(date,'%Y-%m-%d')
		except Exception as e:
			print(e)
			errors.append(f"Date is in wrong format > {date}")

		#input time
		time = request.POST.get('time')
		try:
			#time conversion
			time = datetime.strptime(time,'%H:%M')
		except Exception as e:
			print(e)
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
			print(e)
			errors.append("Date or Time is wrong")

		#input duration hour
		durationHour = request.POST.get('durationHour')
		try:
			#convert to int
			durationHour = int(durationHour)
		except Exception as e:
			print(e)
			errors.append("Duration Hour should be an integer.")

		#input duration minute
		durationMinute = request.POST.get('durationMinute')
		try:
			#convert to int
			durationMinute = int(durationMinute)
		except Exception as e:
			print(e)
			errors.append("Duration Minute should be an integer.")

		#create single duration timedelta object
		try:
			duration = timedelta(hours=durationHour,minutes=durationMinute)
		except Exception as e:
			print(e)
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
				print(e)
				errors.append('Repeat should be an integer.')

		#days list
		days = request.POST.getlist('days')

		#no(infinite)/ end(date)/ number(of meetings)

		#ending date and conversion to utc
		endingdate = request.POST.get('endingDate')
		if(endingdate):
			try:
				endingdate = datetime.strptime(endingdate,'%Y-%m-%d')
				print('endingdate',endingdate)
				utcEndingdate = old_timezone.localize(endingdate).astimezone(new_timezone)
				print('UTC herer',utcEndingdate)
			except Exception as e:
				print(e)
				errors.append(f"Date is in wrong format > {date}")
		else:
			endingdate = dateTimeObj + duration
			print('here',endingdate,timezone,old_timezone,new_timezone)
			try:
				utcEndingdate = old_timezone.localize(endingdate).astimezone(new_timezone)
			except Exception as e:
				print(e)
				errors.append(f"Date is in wrong format > {date}")
		#tutor id
		tutorId = request.POST.get('tutorId')
		try:
			#tutor object for appointment
			tutorObj = SignupTutor.objects.get(sno=int(tutorId))
		except Exception as e:
			print(e)
			errors.append('Tutor Doesnot Exists ({tutorId})')

		daysDump = createReccurance(utcDateTime,duration,recc,pattern,repeat,days,utcEndingdate)
		#checking clashes for student
		try:
			if(checkClashes(studentObj,utcDateTime,duration,recc,pattern,repeat,days,utcEndingdate,daysDump)):
				errors.append("This appontment cannot be created as you already have an appointment during this duration.")
		except Exception as e:
			print(e)
			errors.append("There was an error while creating this appointment for you.")

		#checking clashes for tutor
		try:
			if(checkClashes(tutorObj,utcDateTime,duration,recc,pattern,repeat,days,utcEndingdate,daysDump)):
				errors.append("This appontment cannot be created as this Tutor already have an appointment during this duration.")
		except Exception as e:
			print(e)
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
			print(utcEndingdate)
			appointmentObj = MakeAppointment(
					dateTime    = dateTimeObj,
					duration    = duration,
					timezone    = timezone,
					recc        = recc,
					pattern     = pattern,
					repeat      = repeat,
					days        = days,
					endingDate  = endingdate,
					tutor       = tutorObj,
					student     = studentObj,
					utcDateTime = utcDateTime,
					utcEndingDate=utcEndingdate,
					daysDump     = json.dumps(daysDump, cls=DjangoJSONEncoder)
				)
			appointmentObj.save()
			return JsonResponse({
				'status':1,
				'msg':appointmentObj.sno
				})

	# return JsonResponse({'a':[1,2,3]})
	return HttpResponse("<br><h1 align='center'>¯\\_(ツ)_/¯</h1>")

def loginAll(request):
	return render(request,"tutor/loginAll.html",{})

def searchCoachingCenter(request):
	centers = SignupCoachingCentre.objects.all()

	if request.method == "POST":
		feeVisible = request.POST.get('feeVisible')
		filDistance = request.POST.get('distance')
		if filDistance=='':
			filDistance = 10**3
		la1 = float(request.POST.get('cityLat',0))
		lo1 = float(request.POST.get('cityLng',0))
		searchQuery = Q(showFees=True) if(feeVisible) else Q(showFees=False)
		allData = SignupCoachingCentre.objects.filter(searchQuery)
		finalData = []
		for x in allData:
			la2 = float(x.latitude)
			lo2 = float(x.longitude)
			distance = distanceBwAB((la1,lo1),(la2,lo2)).km
			if(float(filDistance)>=float(distance)):
				finalData.append(x)
		return render(request, 'tutor/searchCoachingCenter.html',{'centers':finalData})

	return render(request, 'tutor/searchCoachingCenter.html',{'centers':centers})

def postNotice(request):
	context = {}
	cookieVAL = request.session.get('CoachingCentre')
	if(cookieVAL==None):
		return HttpResponse("<script>alert('Coaching Center is not logged in.')</script>")
	inst = SignupCoachingCentre.objects.get(s_no=cookieVAL)

	if request.method == "POST":
		title = request.POST.get("title")
		desc = request.POST.get("description")
		batch_id = request.POST.get("batch")

		batch = BatchTiming.objects.get(sno = batch_id)
		newNotice = Notice(
							title = title,
							description = desc,
							batch = batch
							)
		newNotice.save()
		return HttpResponse("Notice Sent Successfully!!")

	context['batches'] = inst.BatchTiming.all()

	return render(request,'tutor/postNotice.html',context)

def getNotices(request):
	# if request.method == "POST":
	cookieVAL = request.session.get('Student')
	if(cookieVAL==None):
		return HttpResponse("<script>alert('Student is not logged in.')</script>")
	stud = SignupStudent.objects.get(snum=cookieVAL)
	notices = {}

	count = request.GET.get("count")
	for inst in stud.AddStudentInst.all():
		detail = inst.AddStudentDetail.all()[0]
		batchname = detail.batch
		centre = SignupCoachingCentre.objects.get(instituteCode=inst.instituteCode)

		batch = centre.BatchTiming.get(sno=batchname)
		for notice in batch.Notice.values():
			print(notice["createdAt"].timestamp())
			notices[notice["createdAt"].timestamp()] = (notice,batch.batchName)
	if len(notices)<=int(count):
		status = 0
	else:
		status = 1
	response = {'count':len(notices),'notices':notices,'status':status}
	return JsonResponse(response)

def addTutorialsInstitute(request):
	cid = request.session['CoachingCentre']
	#print(cid)
	coaching = SignupCoachingCentre.objects.get(s_no=cid)
	courses = AddCourses.objects.filter(coachingCentre = coaching)
	context = {
	'courses':courses
	}
	if request.method == "POST":
		title = request.POST.get('title',"")
		description = request.POST.get('description',"")
		fees = request.POST.get('fees',"")
		duration = request.POST.get("duration","")
		course = request.POST.get("course","")
		feeDisc = request.POST.get("feeDisc","")
		discValidity = request.POST.get("discValidity","")
		discValidity = datetime.strptime(discValidity,'%Y-%m-%d')
		print(title,description,fees,duration,course,feeDisc,discValidity)
		data = TutorialInstitute(
			Title = title,
			Course = AddCourses.objects.get(s_num=course),
			Fees = fees,
			Duration = duration,
			Description = description,
			Validity = discValidity,
			Discount = feeDisc,
			)
		data.save()
		return redirect('addplaylist',data.id)
	return render(request,'tutor/addTutorialsInstitute.html',context)

def addTutorialsInstituteVideos(request,course_id):
	tutorial = TutorialInstitute.objects.get(id=course_id)
	errors = []
	if request.method == "POST":
		video = request.FILES.getlist("video")
		title = request.POST.getlist("title")
		description = request.POST.getlist("description")
		try:
			for item in range(len(title)):
				data = TutorialInstitutePlaylist(
					tutorial = tutorial,
					Title = title[item],
					Description = description[item],
					Video = video[item])
				data.save()
		except:
			errors.append("File Field Must Not be Empty")
			return render(request,'tutor/AddCourseVideos.html',{'errors':errors})
		return redirect('viewtutorials')
	return render(request,'tutor/AddCourseVideos.html')

def ViewTutorials(request):
	cid = request.session['CoachingCentre']
	#print(cid)
	coaching = SignupCoachingCentre.objects.get(s_no=cid)
	courses = AddCourses.objects.filter(coachingCentre = coaching)
	tutorials = []
	for i in courses:
		if TutorialInstitute.objects.filter(Course=i).exists():
			print(TutorialInstitute.objects.filter(Q(Course=i) & Q(Archived=False)))
			tutorials.extend(TutorialInstitute.objects.filter(Q(Course=i) & Q(Archived=False)))

	context = {
	'tutorials':tutorials
	}
	if request.method == "POST":
		ids = request.POST.getlist('ids')
		if len(ids)<1:
			return redirect('viewtutorials')
		for i in ids:
			if TutorialInstitute.objects.filter(id=i).exists():
				tutorial = TutorialInstitute.objects.get(id=int(i))
				tutorial.Archived = True
				tutorial.save()
		return redirect('archivetutorials')
	return render(request,'tutor/viewtutorials.html',context)


def EditTutorialsInstitute(request,course_id):
	cid = request.session['CoachingCentre']
	coaching = SignupCoachingCentre.objects.get(s_no=cid)
	courses = AddCourses.objects.filter(coachingCentre = coaching)
	tutorial = TutorialInstitute.objects.get(id=course_id)
	context = {
	'tutorial':tutorial,
	'courses':courses
	}
	if request.method == "POST":
		title = request.POST.get('title',"")
		description = request.POST.get('description',"")
		fees = request.POST.get('fees',"")
		duration = request.POST.get("duration","")
		course = request.POST.get("course","")
		feeDisc = request.POST.get("feeDisc","")
		discValidity = request.POST.get("discValidity","")
		if title:
			tutorial.Title = title

		if description:
			tutorial.Description = description

		if fees:
			tutorial.Fees = fees

		if duration:
			tutorial.Duration = duration

		if course:
			tutorial.Course = AddCourses.objects.get(s_num=course)

		if feeDisc:
			tutorial.Discount = feeDisc

		if discValidity:
			discValidity = datetime.strptime(discValidity,'%Y-%m-%d')
			tutorial.Validity = discValidity

		tutorial.save()
		return redirect('viewtutorials')
	return render(request,'tutor/editTutorial.html',context)

def DeleteTutorialsInstitute(request,course_id):
	data = TutorialInstitute.objects.get(id=course_id)
	data.delete()
	return redirect('viewtutorials')

def ArchiveTutorials(request):
	cid = request.session['CoachingCentre']
	#print(cid)
	coaching = SignupCoachingCentre.objects.get(s_no=cid)
	courses = AddCourses.objects.filter(coachingCentre = coaching)
	tutorials = []
	for i in courses:
		if TutorialInstitute.objects.filter(Course=i).exists():
			print(TutorialInstitute.objects.filter(Q(Course=i) & Q(Archived=False)))
			tutorials.extend(TutorialInstitute.objects.filter(Q(Course=i) & Q(Archived=True)))

	context = {
	'tutorials':tutorials
	}
	if request.method == "POST":
		ids = request.POST.getlist('ids')
		if len(ids)<1:
			return redirect('archivetutorials')
		for i in ids:
			if TutorialInstitute.objects.filter(id=i).exists():
				tutorial = TutorialInstitute.objects.get(id=int(i))
				tutorial.Archived = False
				tutorial.save()
		return redirect('viewtutorials')
	return render(request,'tutor/ArchievedTutorials.html',context)

def WatchTutorialsInstitute(request,course_id):
	cid = request.session['CoachingCentre']
	coaching = SignupCoachingCentre.objects.get(s_no=cid)
	courses = AddCourses.objects.filter(coachingCentre = coaching)
	tutorial = TutorialInstitute.objects.get(id=course_id)
	if request.session.has_key(f"Watching{course_id}"):
		start = request.session[f"Watching{course_id}"]
	else:
		if TutorialInstitutePlaylist.objects.filter(tutorial=tutorial).exists():
			start = TutorialInstitutePlaylist.objects.filter(tutorial=tutorial).first().Video.url
			request.session[f"Watching{course_id}"] = start

	total_length = 0

	if TutorialInstitutePlaylist.objects.filter(tutorial=tutorial).exists():
		for item in TutorialInstitutePlaylist.objects.filter(tutorial=tutorial):
			total_length += item.Clip_Duration()

	total_length = f"{total_length} min"
	context = {
	'tutorial':tutorial,
	'start':start,
	'total_length':total_length
	}
	return render(request,'tutor/watchTutorial.html',context)

def EditTutorialsInstituteVideos(request,playlist_id):
	tutorial = TutorialInstitutePlaylist.objects.get(id=playlist_id)
	context = {
	'tutorial':tutorial,
	}
	if request.method == "POST":
		video = request.POST.get('video','')
		title = request.POST.get('title',"")
		description = request.POST.get('description',"")
		if title:
			tutorial.Title = title

		if description:
			tutorial.Description = description

		if video:
			tutorial.Video = video
		tutorial.save()
		return redirect('viewtutorial',tutorial.tutorial.id)
	return render(request,'tutor/editTutorialVideos.html',context)


def DeleteTutorialsInstituteVideos(request,playlist_id):
	data = TutorialInstitutePlaylist.objects.get(id=playlist_id)
	data.delete()
	return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def addTutorialsTutor(request):
	sno = request.session['Tutor']
	if SignupTutor.objects.filter(sno = sno).exists():
		tutor = SignupTutor.objects.get(sno = sno)
	else:
		return redirect('landing')
	context = {
	}
	if request.method == "POST":
		title = request.POST.get('title',"")
		description = request.POST.get('description',"")
		fees = request.POST.get('fees',"")
		duration = request.POST.get("duration","")
		feeDisc = request.POST.get("feeDisc","")
		discValidity = request.POST.get("discValidity","")
		discValidity = datetime.strptime(discValidity,'%Y-%m-%d')
		data = TutorialTutors(
			Title = title,
			Tutor = tutor,
			Fees = fees,
			Duration = duration,
			Description = description,
			Validity = discValidity,
			Discount = feeDisc,
			)
		data.save()
		return redirect('addvideosTutor',data.id)
	return render(request,'tutor/addTutorialsTutor.html',context)

def addTutorialsTutorVideos(request,course_id):
	tutorial = TutorialTutors.objects.get(id=course_id)
	errors = []
	if request.method == "POST":
		video = request.FILES.getlist("video")
		title = request.POST.getlist("title")
		description = request.POST.getlist("description")
		print(video,title)
		try:
			for item in range(len(title)):
				data = TutorialTutorsPlaylist(
					tutorial = tutorial,
					Title = title[item],
					Description = description[item],
					Video = video[item])
				data.save()
		except:
			errors.append("File Field Must Not be Empty")
			return render(request,'tutor/AddTutorCourseVideos.html',{'errors':errors})
		return redirect('viewtutorialstutor')
	return render(request,'tutor/AddTutorCourseVideos.html')


def ViewTutorialsTutor(request):
	sno = request.session['Tutor']
	if SignupTutor.objects.filter(sno = sno).exists():
		tutor = SignupTutor.objects.get(sno = sno)
	else:
		return redirect('landing')
	tutorials = TutorialTutors.objects.filter(Q(Tutor=tutor) & Q(Archived=False))
	context = {
	'tutorials':tutorials
	}
	if request.method == "POST":
		ids = request.POST.getlist('ids')
		if len(ids)<1:
			return redirect('viewtutorialstutor')
		for i in ids:
			if TutorialTutors.objects.filter(id=i).exists():
				tutorial = TutorialTutors.objects.get(id=int(i))
				tutorial.Archived = True
				tutorial.save()
			print('yes')
		return redirect('viewtutorialstutor')
	return render(request,'tutor/viewTutorialsTutor.html',context)



def ArchiveTutorialsTutor(request):
	sno = request.session['Tutor']
	if SignupTutor.objects.filter(sno = sno).exists():
		tutor = SignupTutor.objects.get(sno = sno)
	else:
		return redirect('landing')
	tutorials = TutorialTutors.objects.filter(Q(Tutor=tutor) & Q(Archived=True))
	context = {
	'tutorials':tutorials
	}
	if request.method == "POST":
		ids = request.POST.getlist('ids')
		if len(ids)<1:
			return redirect('archivetutorialstutor')
		for i in ids:
			if TutorialTutors.objects.filter(id=i).exists():
				tutorial = TutorialTutors.objects.get(id=int(i))
				tutorial.Archived = False
				tutorial.save()
		return redirect('archivetutorialstutor')
	return render(request,'tutor/ArchievedTutorialsTutor.html',context)

def EditTutorialsTutor(request,course_id):
	sno = request.session['Tutor']
	if SignupTutor.objects.filter(sno = sno).exists():
		tutor = SignupTutor.objects.get(sno = sno)
	else:
		return redirect('landing')
	tutorial = TutorialTutors.objects.get(id=course_id)
	context = {
	'tutorial':tutorial,
	}
	if request.method == "POST":
		title = request.POST.get('title',"")
		description = request.POST.get('description',"")
		fees = request.POST.get('fees',"")
		duration = request.POST.get("duration","")
		feeDisc = request.POST.get("feeDisc","")
		discValidity = request.POST.get("discValidity","")
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
			discValidity = datetime.strptime(discValidity,'%Y-%m-%d')
			tutorial.Validity = discValidity

		tutorial.save()
		return redirect('viewtutorialstutor')
	return render(request,'tutor/editTutorialTutor.html',context)

def DeleteTutorialsTutor(request,course_id):
	data = TutorialTutors.objects.get(id=course_id)
	data.delete()
	return redirect('viewtutorialstutor')


def WatchTutorialsTutor(request,course_id):
	sno = request.session['Tutor']
	if SignupTutor.objects.filter(sno = sno).exists():
		tutor = SignupTutor.objects.get(sno = sno)
	else:
		return redirect('landing')
	tutorial = TutorialTutors.objects.get(id=course_id)

	if request.session.has_key(f"WatchingTutor{course_id}"):
		start = request.session[f"WatchingTutor{course_id}"]
	else:
		if TutorialTutorsPlaylist.objects.filter(tutorial=tutorial).exists():
			start = TutorialTutorsPlaylist.objects.filter(tutorial=tutorial).first().Video.url
			request.session[f"WatchingTutor{course_id}"] = start
	total_length= 0

	if TutorialTutorsPlaylist.objects.filter(tutorial=tutorial).exists():
		for item in TutorialTutorsPlaylist.objects.filter(tutorial=tutorial):
			total_length += item.Clip_Duration()

	total_length = f"{total_length}min"
	context = {
	'tutorial':tutorial,
	'start':start,
	'total_length':total_length
	}
	return render(request,'tutor/watchTutorialTutor.html',context)

def DeleteTutorialsTutorVideos(request,playlist_id):
	data = TutorialTutorsPlaylist.objects.get(id=playlist_id)
	data.delete()
	return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def EditTutorialsTutorVideos(request,playlist_id):
	tutorial = TutorialTutorsPlaylist.objects.get(id=playlist_id)
	context = {
	'tutorial':tutorial,
	}
	if request.method == "POST":
		video = request.POST.get('video','')
		title = request.POST.get('title',"")
		description = request.POST.get('description',"")
		if title:
			tutorial.Title = title
		if description:
			tutorial.Description = description
		if video:
			tutorial.Video = video
		tutorial.save()
		return redirect('viewtutorialtutor',tutorial.tutorial.id)
	return render(request,'tutor/editTutorialVideosTutor.html',context)


def SearchCourses(request):
	tutorials = TutorialTutors.objects.all()
	extra  = TutorialInstitute.objects.all()
	courses = TutorialInstitute.objects.all()
	if request.method=='POST':
		coursetype = request.POST.get('type','')
		duration = request.POST.get('duration','')
		fees = request.POST.get('fees','')
		if coursetype:
			extra = TutorialInstitute.objects.all().filter(Q(Course=AddCourses.objects.get(s_num=coursetype)))
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
				extra = extra.filter(Q(Fees__gte=fees[0]) & Q(Fees__lte=fees[1]))
			if tutorials.exists():
				tutorials = tutorials.filter(Q(Fees__gte=fees[0]) & Q(Fees__lte=fees[1]))

		if tutorials and extra:
			tutorials = tutorials.union(extra)
		elif extra:
			tutorials=extra
		else:
			tutorials=tutorials
		context = {
		'tutorials':tutorials,
		'courses':courses
		}
		return render(request,'tutor/SearchCourses.html',context)
	tutorials = tutorials.union(extra).order_by('Title')
	context = {
	'tutorials':tutorials,
	'courses':courses
	}
	return render(request,'tutor/SearchCourses.html',context)

def WatchTutorTutorials(request,course_id):
	tutorial =TutorialTutors.objects.get(id=course_id)
	total_length = 0
	if TutorialTutorsPlaylist.objects.filter(tutorial=tutorial).exists():
		for item in TutorialTutorsPlaylist.objects.filter(tutorial=tutorial):
			total_length += item.Clip_Duration()
	total_length = f"{total_length}min"
	start = TutorialTutorsPlaylist.objects.filter(tutorial=tutorial).first().Video.url
	context = {
	'tutorial':tutorial,
	'start':start,
	'total_length':total_length
	}
	return render(request,'tutor/watchTutorialStudent.html',context)

def WatchInstituteTutorials(request,course_id):
	tutorial =TutorialInstitute.objects.get(id=course_id)
	total_length = 0
	if TutorialInstitutePlaylist.objects.filter(tutorial=tutorial).exists():
		for item in TutorialInstitutePlaylist.objects.filter(tutorial=tutorial):
			total_length += item.Clip_Duration()
	total_length = f"{total_length}min"
	start = TutorialInstitutePlaylist.objects.filter(tutorial=tutorial).first().Video.url
	context = {
	'tutorial':tutorial,
	'start':start,
	'total_length':total_length
	}
	return render(request,'tutor/watchTutorialStudent.html',context)

def forgotpass(request):
	if request.method=="POST":
		if "first" in request.POST:
			email = request.POST.get('username')
			type = request.POST.get('type')

			if type=="Coaching":
				user = SignupCoachingCentre.objects.get(email=email).s_no
			elif type=="Tutor":
				user = SignupTutor.objects.get(email=email).sno
			else:
				user = SignupStudent.objects.get(email=email).snum

			if user is not None:
				digits = "0123456789"
				otp_code = ""
				for i in range(8) :
					otp_code += digits[math.floor(random.random() * 10)]
				#send OTP EMAIL
				msg = EmailMessage('Reset Password',"Your OTP for changing password is "+str(otp_code), to=[email])
				msg.send()

				otp = OTP(
					otp = otp_code,
					user = user,
					type = type
					)

				return render(request,'tutor/forgotpassCoaching.html',{'trial':"1",'user':user,'type':type})
			else:
				return render(request,'tutor/forgotpassCoaching.html',{"trial":"0"})

		if "second" in request.POST:
			otp = request.POST.get('otp')
			user = request.POST.get('user')
			type = request.POST.get('type')
			password = request.POST.get('password')
			cpassword = request.POST.get('cpassword')

			if type=="Coaching":
				user = SignupCoachingCentre.objects.get(s_no=s_no)
			elif type=="Tutor":
				user = SignupTutor.objects.get(sno=user)
			else:
				user = SignupStudent.objects.get(snum=user)

			otp_code = OTP.objects.get(user=user,type=type)
			if (otp_code is not None) and (user is not None) and (password==cpassword) and (otp==otp_code.otp):
				user.password = password
				user.save()
				otp_code.delete()
			else:
				return HttpResponse("Invalid Info")

	return render(request,'tutor/forgotpass.html',{"trial":"0"})

def SearchBar(request):
	tutorials = TutorialTutors.objects.all()
	extra  = TutorialInstitute.objects.all()
	courses = TutorialInstitute.objects.all()
	if request.method=='POST':
		searchInput = request.POST.get("course","")
		if searchInput:
			if tutorials:
				tutorials = tutorials.filter(Q(Title__icontains=searchInput) | Q(Description__icontains=searchInput))
			if extra:
				extra = extra.filter(Q(Title__icontains=searchInput) | Q(Description__icontains=searchInput))

		if tutorials and extra:
			tutorials = tutorials.union(extra)
		elif extra:
			tutorials=extra
		else:
			tutorials=tutorials
		context = {
		'tutorials':tutorials,
		'courses':courses,
		'filter':True
		}
		return render(request,'tutor/SearchCourses.html',context)
	tutorials = tutorials.union(extra).order_by('Title')
	context = {
	'tutorials':tutorials,
	'courses':courses,
	'filter':True
	}
	return render(request,'tutor/SearchCourses.html',context)

def getOTP(request):
	if request.method=="POST":
		email = request.POST.get('email')
		if email:
			digits = "0123456789"
			otp_code = ""
			for i in range(8) :
				otp_code += digits[math.floor(random.random() * 10)]
			#send OTP EMAIL
			msg = EmailMessage('Validate Email',"Your OTP for validating Email is "+str(otp_code), to=[email])
			msg.send()

			type= 'any'
			otp = OTP(
				otp = otp_code,
				user = email,
				type = type
				)
			return JsonResponse({'status':1})
		else:
			return JsonResponse({'status':0})


def PostReviewTutor(request,Course_id):
	cid = request.session['Student']
	student = SignupStudent.objects.get(snum=cid)
	tutorial = TutorialTutors.objects.get(id=Course_id)
	if request.method == "POST":
		rating =request.POST.get("rating","")
		comment = request.POST.get("comment","")
		print(rating,comment)
		data = ReviewsTutor(
			Tutor = tutorial,
			Student = student,
			Review=comment,
			Rating = rating,
			)
		data.save()
		return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
	return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def PostReviewInstitute(request,Course_id):
	cid = request.session['Student']
	student = SignupStudent.objects.get(snum=cid)
	tutorial = TutorialInstitute.objects.get(id=Course_id)
	if request.method == "POST":
		rating =request.POST.get("rating","")
		comment = request.POST.get("comment","")
		print(rating,comment)
		data = ReviewsInstitute(
			Institute = tutorial,
			Review=comment,
			Student = student,
			Rating = rating,
			)
		data.save()
		return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
	return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))