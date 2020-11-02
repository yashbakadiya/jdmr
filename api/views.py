from rest_framework import generics
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *
from tutor.models import *
from django.views.decorators.csrf import csrf_exempt
# from tutor.views import encryptPassword, decryptPassword
from django.db.models import Q
from collections import OrderedDict
from itertools import chain
from django.db.models import Avg, Max, Min, Sum

@api_view(["GET"])
# Test API call
def logincoachingentre(request,username,password):
	data = {}
	print(request.data)
	if request.method=="GET":
		inst_names = SignupCoachingCentre.objects.values('instituteName', 'password','email','s_no','photo','avatar')
		for item in inst_names:
			if ((item['instituteName'] == username or item['email'] == username) and item['password'] == password):
				login = LoginCoachingCentre(username=username,password=password)
				login.save()
				request.session['CoachingCentre'] = item['s_no']
				data["Success"] = "User has successfully logged In"
				return Response(data)
		data["error"] = "Invalid Credentials, Please try again"
	return Response(data)


@api_view(["POST",])
def signupCoachingCentre(request):
	serializer = CoachingCenterSerializer(data=request.data)
	if serializer.is_valid():
		serializer.save()
		details["Success"] = "User Created Successfully"
	else:
		details["error"] = "Error Occured!Try Again"
		return Response(details)


# Add and Save Courses
@api_view(["GET","POST"])
def CoursesCentre(request):
	c_id = request.session['CoachingCentre']
	try:
		center = SignupCoachingCentre.objects.get(s_no=c_id)
	except Exception as e:
		data["error"] = e
		return Response(data)
	if request.method == "GET":
		courses = AddCourses.objects.filter(coachingCentre=center)
		serializer = CoachingCenterCoursesSerializer(courses,many=True)
		return Response(serializer.data)

	if request.method == "POST":
		details = request.data
		courseName = details['courseName']
		count= AddCourses.objects.all().count()
		count=count+1
		name= details['courseName']
		ch1=str("%03d" % count)
		ch2=str(name[0:2])
		cid=ch2+ch1
		forclass1 = details['forclass']
		forclass=', '.join(forclass1)
		addCourses = AddCourses(courseName=courseName,cid=cid,forclass=forclass,coachingCentre= center)
		addCourses.save()
		data["success"] = "Course Added Successfully"
		return Response(data)

# edit and Delete Courses
@api_view(['PUT','DELETE'])
def CoursesCentreEdit(request,pk):
	data = {}
	if request.method == "DELETE":
		course = AddCourses.objects.get(s_num=pk)
		course.delete()
		data["success"] = "Course Deleted Successfully" 
		return Response(data)

	if request.method == "PUT":
		course = AddCourses.objects.get(s_num=pk)
		serializer = CoachingCenterCoursesSerializer(instance = course, data=request.data)
		if serializer.is_valid():
			serializer.save()
			data["success"] = "Course Added Successfully"
			return Response(data)
		data["error"] = "data Couldn't be saved "
		return Response(data)



# Archived Courses
@api_view(["GET","POST"])
def ArchivedCoursesCentre(request):
	c_id = request.session['CoachingCentre']
	try:
		center = SignupCoachingCentre.objects.get(s_no=c_id)
	except Exception as e:
		data["error"] = e
		return Response(data)
	if request.method == "GET":
		courses = ArchiveCourses.objects.filter(coachingCentre=center)
		serializer = CoachingCenterCoursesSerializer(courses,many=True)
		return Response(serializer.data)

	if request.method == "POST":
		course = AddCourses.objects.get(s_num=request.data["id"])
		Archive = ArchiveCourses(
			crid = course.cid,
			crName = course.courseName,
			crclass = course.forclass,
			coachingCentre = center)
		Archive.save()
		course.delete()
		data["success"] = "Course Added Successfully"
		return Response(data)


# Archived Courses
@api_view(["POST"])
def RemoveArchivedCoursesCentre(request):
	c_id = request.session['CoachingCentre']
	try:
		center = SignupCoachingCentre.objects.get(s_no=c_id)
	except Exception as e:
		data["error"] = "Coaching Center is not logged In"
		return Response(data)
	if request.method == "POST":
		Archive = ArchiveCourses.objects.get(s_num=request.data["id"])
		course = AddCourses(
			cid = Archive.crid,
			courseName = Archive.crName,
			forclass = Archive.crclass,
			coachingCentre = center)
		Archive.delete()
		course.save()
		data["success"] = "Course Added Successfully"
		return Response(data)

@api_view(["GET","POST"])
def TeachingTypeCenter(request):
	c_id = request.session['CoachingCentre']
	try:
		center = SignupCoachingCentre.objects.get(s_no=c_id)
	except Exception as e:
		data["error"] = "Coaching Center is not logged In"
		return Response(data)
	if request.method == "GET":
		courses = AddCourses.objects.filter(coachingCentre=center)
		teachingtype = []
		for course in courses:
			if TeachingType.objects.filter(course=course).exists():
				teachingtype.extend(TeachingType.objects.filter(course=course))
			else:
				pass
		serializer = CoachingCenterTeachingTypeSerializer(teachingtype,many=True)
		return Response(serializer.data)
	
	if request.method=="POST":
		courseName = request.data['courseName']
		forclass1 = request.data['forclass']
		forclass=', '.join(forclass1)
		teachType1 = request.data['check']
		teachType='\n'.join(teachType1)
		duration1 = request.data['duration']
		duration='\n'.join(duration1)
		print(duration)
		timePeriod1 = request.data['time']
		timePeriod='\n'.join(timePeriod1)
		print(timePeriod)
		alreadyExists = TeachingType.objects.filter(courseName=courseName,forclass=forclass,teachType=teachType,duration=duration,timePeriod=timePeriod)
		if(alreadyExists):
			data["error"] =  "Already exists"
			return Response(data)
		course = inst.AddCourses.filter(Q(courseName=courseName))[0]
		if course:
			teachingtype = TeachingType(course=course,courseName=courseName,forclass=forclass,teachType=teachType,duration=duration,timePeriod=timePeriod)
			teachingtype.save()
			data["success"] = "data Saved Successfully"
			return Response(data)

# edit and Delete Courses
@api_view(['PUT','DELETE'])
def TeachingTypeEdit(request,pk):
	data = {}
	if request.method == "DELETE":
		course = TeachingType.objects.get(s_num=pk)
		course.delete()
		data["success"] = "Course Deleted Successfully" 
		return Response(data)

	if request.method == "PUT":
		course = TeachingType.objects.get(s_num=pk)
		serializer = CoachingCenterTeachingTypeSerializer(instance = course, data=request.data)
		if serializer.is_valid():
			serializer.save()
			data["success"] = "Saved Successfully"
			return Response(data)
		data["error"] = "data Couldn't be saved "
		return Response(data)



@api_view(["GET","POST"])
def BatchTimingCenter(request):
	c_id = request.session['CoachingCentre']
	try:
		center = SignupCoachingCentre.objects.get(s_no=c_id)
	except Exception as e:
		data["error"] = "Coaching Center is not logged In"
		return Response(data)
	if request.method == "GET":
		batches = BatchTiming.objects.filter(coachingCenter=center)
		serializer = CoachingCenterBatchTimingSerializer(batches,many=True)
		return Response(serializer.data)
	
	if request.method=="POST":
			serializer = CoachingCenterBatchTimingSerializer(data=request.data)
			if serializer.is_valid():
				serializer.save()
				details["Success"] = "Batch Created Successfully"
			else:
				details["error"] = "Error Occured!Try Again"
				return Response(details)

# edit and Delete Courses
@api_view(['PUT','DELETE'])
def BatchTimingEdit(request,pk):
	data = {}
	if request.method == "DELETE":
		course = BatchTiming.objects.get(s_num=pk)
		course.delete()
		data["success"] = "Batch Deleted Successfully" 
		return Response(data)

	if request.method == "PUT":
		course = BatchTiming.objects.get(s_num=pk)
		serializer = CoachingCenterBatchTimingSerializer(instance = course, data=request.data)
		if serializer.is_valid():
			serializer.save()
			data["Success"] = "Batch Updated Successfully"
			return Response(data)
		else:
			data["error"] = "error occured! Try Again"
			return Response(data)

@api_view(["GET","POST"])
def AddFeesCenter(request):
	c_id = request.session['CoachingCentre']
	try:
		center = SignupCoachingCentre.objects.get(s_no=c_id)
	except Exception as e:
		data["error"] = "Coaching Center is not logged In"
		return Response(data)
	if request.method == "GET":
		courses = AddCourses.objects.filter(coachingCentre=center)
		fees = []
		for course in courses:
			if AddFeesC.objects.filter(course=course).exists():
				fees.extend(AddFeesC.objects.filter(course=course))
			else:
				pass
		serializer = CoachingCenterFeesSerializer(fees,many=True)
		return Response(serializer.data)
	
	if request.method=="POST":
		courseName = request.data['courseName']
		forclass = request.data['forclass']
		teachType = request.data['teachType']
		duration = request.data['duration']
		fee_amt = request.data['fee_amt']
		tax = request.data['tax']
		final_amt = request.data['final_amt']
		no_of_installment = request.data['no_of_installment']
		typeOfCharge = request.data['typeOfCharge']
		extra_charge = request.data['extra_charge']
		feeDisc = request.data['feeDisc']
		discValidity = request.data['discValidity']
		final_amount = request.data['final_amount']
		course = request.data['course']
		discValidity = datetime.strptime(discValidity,'%Y-%m-%d')
		try:
			course = AddCourses.objects.get(s_num=course)
			addfees = AddFeesC(
				course=course,
				courseName=courseName,
				forclass=forclass,
				teachType=teachType,
				duration=duration,
				fee_amt=fee_amt,
				tax=tax,
				final_amt=final_amt,
				no_of_installment=no_of_installment,
				typeOfCharge=typeOfCharge,
				extra_charge=extra_charge,
				feeDisc=feeDisc,
				discValidity=discValidity,
				final_amount=final_amount)
			addfees.save()
			data["success"] = "data Saved Successfully"
			return Response(data)
		except:
			data["error"] = "error occured!Enter correct details"
			return Response(data)	

# edit and Delete Courses
@api_view(['PUT','DELETE'])
def AddFeesEdit(request,pk):
	data = {}
	if request.method == "DELETE":
		fees = AddFeesC.objects.get(sno=pk)
		fees.delete()
		data["success"] = "Fees Deleted Successfully" 
		return Response(data)

	if request.method == "PUT":
		fees = AddFeesC.objects.get(sno=pk)
		details = request.data
		validity = details['discValidity']
		discValidity = datetime.strptime(validity,'%Y-%m-%d')
		details['discValidity'] = discValidity
		serializer = CoachingCenterTeachingTypeSerializer(instance = fees, data=details)
		if serializer.is_valid():
			serializer.save()
			data["success"] = "Saved Successfully"
			return Response(data)
		data["error"] = "data Couldn't be saved "
		return Response(data)

# Archived Fees
@api_view(["POST"])
def ArchiveFeesCentre(request):
	Archive = AddFeesC.objects.get(sno=request.data["id"])
	fees = ArchiveFees(		
		course=Archive.course,
		courseName=Archive.courseName,
		forclass=Archive.forclass,
		teachType=Archive.teachType,
		duration=Archive.duration,
		fee_amt=Archive.fee_amt,
		tax=Archive.tax,
		final_amt=Archive.final_amt,
		no_of_installment=Archive.no_of_installment,
		typeOfCharge=Archive.typeOfCharge,
		extra_charge=Archive.extra_charge,
		feeDisc=Archive.feeDisc,
		discValidity=Archive.discValidity,
		final_amount=Archive.final_amount)
	Archive.delete()
	fees.save()
	data["success"] = "Moved To Archive"
	return Response(data)


# Remove Archived Fees
@api_view(["POST"])
def RemoveArchiveFeesCentre(request):
	Archive = ArchiveFees.objects.get(sno=request.data["id"])
	fees = AddFeesC(		
		course=Archive.course,
		courseName=Archive.courseName,
		forclass=Archive.forclass,
		teachType=Archive.teachType,
		duration=Archive.duration,
		fee_amt=Archive.fee_amt,
		tax=Archive.tax,
		final_amt=Archive.final_amt,
		no_of_installment=Archive.no_of_installment,
		typeOfCharge=Archive.typeOfCharge,
		extra_charge=Archive.extra_charge,
		feeDisc=Archive.feeDisc,
		discValidity=Archive.discValidity,
		final_amount=Archive.final_amount)
	Archive.delete()
	fees.save()
	data["success"] = "Removed From Archive"
	return Response(data)

@api_view(["POST"])
def SearchFeesCenter(request):
	srch = request.data['search']
	match = AddFeesC.objects.filter(Q(teachType__icontains=srch)| Q(courseName__icontains=srch) | Q(duration__icontains=srch))
	serializer = CoachingCenterFeesSerializer(match,many=True)
	return Response(serializer.data)

@api_view(["POST"])
def SubmitFeesCenter(request):
	c_id = request.session['CoachingCentre']
	try:
		center = SignupCoachingCentre.objects.get(s_no=c_id)
	except Exception as e:
		data["error"] = "Coaching Center is not logged In"
		return Response(data)
	name = request.data['search']
	print(name)
	data = AddStudentInst.objects.filter((Q(conector__username__contains=name) | Q(conector__firstName__contains=name) |
					Q(conector__lastName__contains=name) | Q(conector__email__contains=name)) & Q(instituteName=center.instituteName))
	print(data)
	serializer = CoachingCenterAddStudentInstSerializer(data,many=True)
	return Response(serializer.data)

@api_view(["POST"])
def SearchTutorCenter(request):
	data={}
	c_id = request.session['CoachingCentre']
	try:
		center = SignupCoachingCentre.objects.get(s_no=c_id)
	except Exception as e:
		data["error"] = "Coaching Center is not logged In"
		return Response(data)
	name = request.data['search']
	match = SignupTutor.objects.filter(Q(username__icontains=name) | Q(email__icontains=name))
	print(match)
	cleaneddata = []
	# iterating over all matching queres
	for x in match:
		# iteration over all mathing enrollTutors objects
		for y in x.enrollTutors.all():
			if(center.instituteCode == y.instituteCode):
				break
		else:
			cleaneddata.append(x)
	if cleaneddata:
		serializer = CoachingCenterenrollTutorsSerializer(cleaneddata,many=True)
		return Response(serializer.data)
	else:
		data["error"] = "No user Found"
		return Response(data)



@api_view(["GET","POST"])
def addTutors(request):
	data = {}
	c_id = request.session['CoachingCentre']
	try:
		center = SignupCoachingCentre.objects.get(s_no=c_id)
	except Exception as e:
		data["error"] = "Coaching Center is not logged In"
		return Response(data)

	if request.method == "GET":
		tutors = enrollTutors.objects.filter(instituteName=center.instituteName)
		serializer =  CoachingCenterenrollTutorsSerializer(tutors,many=True)
		return Response(serializer.data)

	if request.method == "POST":
		firstName = request.data.get('firstName', '')
		lastName = request.data.get('lastName', '')
		email = request.data.get('email', '')
		phone = request.data.get('phone', '')
		password = phone
		distance = request.data.get('distance',0)
		username = email
		count= SignupTutor.objects.all().count()
		count=count+1
		name= request.data.get('firstName', '')
		ch1=str("%04d" % count)
		ch2=str(name[0:2])
		tutorCode=ch2+ch1
		location = request.data.get('location', '')
		lat = request.data.get('cityLat', 1)
		lng = request.data.get('cityLng', 1)
		if firstName.isalpha() == False | lastName.isalpha() == False:
			data['error'] = "Name must be alphabetical"
			return Response(data)
		if len(phone) != 10:
			data['error'] = "Phone Number must be 10 digits"
			return Response(data)
		if phone.isdigit() == False:
			data['error'] = "Phone Number must be numeric"
			return Response(data)
		if distance.isdigit() == False:
			data['error'] = "Distance must be numeric"
			return Response(data)
		if SignupTutor.objects.filter(email=email).exists():
			data['error'] = "Email Already Exists"
			return Response(data)
		if SignupTutor.objects.filter(phone=phone).exists():
			data['error'] = "Phone No is Already Registered"
			return Response(data)
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
		signupTutor.save()
		match = enrollTutors(
			signUp          = signupTutor,
			instituteName   = center.instituteName,
			instituteCode   = center.instituteCode
			)
		match.save()
		ctn = request.data.get('ctn_combined')
		cn = request.data.get('cn_combined')
		ttn = request.data.getlist('ttn_combined')
		ttn = [x.replace("\r","") for x in ttn]
		availability = request.data.get('availability')
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
				savTut = AddTutorsInst(
						username=match,
						cid = center ,
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
					data['error'] = "User couldn't be Saved"
					return Response(data)



@api_view(["DELETE"])
def DeleteTutorInstitute(request,pk):
	data = {}
	if request.method == "DELETE":
		object = enrollTutors.objects.get(sno=pk)
		object.delete()
		data["success"] = "Tutor Deleted Successfully"
		return Response(data)


@api_view(["PUT"])
def EditTutorInstitute(request,pk):
	data= {}
	c_id = request.session['CoachingCentre']
	try:
		center = SignupCoachingCentre.objects.get(s_no=c_id)
	except Exception as e:
		data["error"] = "Coaching Center is not logged In"
		return Response(data)

	if(request.method=='PUT'):
		ctn = request.data.get('ctn_combined')
		cn = request.data.get('cn_combined')
		ttn = request.data.get('ttn_combined')
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

		signup_tutor = SignupTutor.objects.get(sno=pk).enrollTutors.all()[0].AddTutorsInst.all()
		usn = SignupTutor.objects.get(sno=pk).enrollTutors.all()[0]
		for x in signup_tutor:
			x.delete()
		for x in range(len(ttn)):
			signup_tutor = SignupTutor.objects.get(sno=sno)
			savTut = AddTutorsInst(
					username=usn,
					cid = center ,
					courseTaught = ctn[x] ,
					forclass = cn[x] ,
					teachType = ttn[x] ,
					availability = availability
				)
			savTut.save()
		NewUsername = request.data.get("NewUsername")
		NewEmail = request.data.get("NewEmail")
		NewPassword = request.data.get("NewPassword")
		NewPhone = request.data.get("NewPhone")
		updateTutorObj = SignupTutor.objects.get(sno=pk)
		updateTutorObj.username = NewUsername
		updateTutorObj.email = NewEmail
		updateTutorObj.password = NewPassword
		updateTutorObj.phone = NewPhone
		updateTutorObj.save()
		data["success"] = "data saved successfully"
		return Response(data)

@api_view(["POST"])
def ArchiveTutors(request,pk):
	data = {}
	if request.method=="POST":
		tutObj = SignupTutor.objects.get(sno=pk)
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
		data["success"] = "archived tutor successfully"
		return Response(data)


@api_view(["GET"])
def archiveTutorList(request):
	tutor = ArchiveTutors.objects.all()
	serializer = CoachingCenterArchiveTutorsSerializer(tutor,many=True)
	return Response( serializer.data)

@api_view(["DELETE"])
def deleteArchiveTutor(request,pk):
	data = {}
	try:
		obj = ArchiveTutors.objects.get(sno=pk)
		obj.delete()
		data["success"] = "Object Deleted Successfully"
	except Exception as e:
		data["error"] = f"{e}"
	return Response(data)

@api_view(["POST"])
def addStudents(request):
	data={}
	if request.method=="POST":
		firstName = request.data.get('firstName', '')
		lastName = request.data.get('lastName', '')
		email = request.data.get('email', '')
		username = email
		phone = request.data.get('phone', '')
		password = phone
		count= SignupStudent.objects.all().count()
		count=count+1
		name= request.data.get('firstName', '')
		ch1=str("%04d" % count)
		ch2=str(name[0:2])
		studentCode=ch2+ch1
		schoolName = request.data.get('schoolName', '')
		location = request.data.get('schoolName', '')
		lat = request.data.get('cityLat', 1)
		lng = request.data.get('cityLng', 1)

		if firstName.isalpha() == False | lastName.isalpha() == False | schoolName.isalpha() == False:
			data["error"] = "Name must be alphabetical"
			return Response(data)
		if len(phone) != 10:
			data["error"] = "Phone Number must be 10 digits"
			return Response(data)
		if SignupStudent.objects.filter(email=email).exists():
			data["error"] = "Student with This Email Exists"
			return Response(data)
		if SignupStudent.objects.filter(phone=phone).exists():
			data["error"] = "Phone Number is Already Registered"
			return Response(data)
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
		c_id = request.session['CoachingCentre']
		try:
			center = SignupCoachingCentre.objects.get(s_no=c_id)
		except Exception as e:
			data["error"] = "Coaching Center is not logged In"
			return Response(data)
		addSI = AddStudentInst(
				username=b.username,
				instituteName=centre.instituteName,
				instituteCode=centre.instituteCode,
				conector = b
			)
		addSI.save()
		ctn = request.data.getlist('ctn_combined')
		cn = request.data.getlist('cn_combined')
		ttn = request.data.getlist('ttn_combined')
		ttn = [x.replace("\r","") for x in ttn]
		batchName = request.data.get('batchN_combined')
		feeDis = request.data.get('feedis_combined')
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
		data["Success"] = "data saved successfully!"
		return Response(data)

@api_view(["GET"])
def viewStudents(request):
	c_id = request.session['CoachingCentre']
	try:
		center = SignupCoachingCentre.objects.get(s_no=c_id)
	except Exception as e:
		data["error"] = "Coaching Center is not logged In"
		return Response(data)
	students = AddStudentInst.objects.filter(Q(instituteName=center.instituteName))
	params = {'students':students}
	detials = []
	try:
		for student in students:
			if AddStudentDetail.objects.filter(username=student).exists():
				detials.extend(AddStudentDetail.objects.filter(username=student))
			else:
				detials.append("")
	except:
		detials =[]
	serializer =  CoachingCenterAddStudentInstSerializer(students,many=True)
	return Response(serializer.data)

@api_view(["POST"])
def deleteStudent(request,sno):
	data = {}
	try:
		obj = AddStudentInst.objects.get(snum=sno)
		obj.delete()
		data["success"] = "Object deleted Successfully"
	except Exception as e:
		data["error"] = f"{e}"
	return Response(data)

@api_view(["POST"])
def deleteArchiveStudent(request,sno):
	data = {}
	try:
		ArchiveStudents.objects.get(snum=sno).delete()
		data["success"] = "Object deleted Successfully"
	except:
		data["error"] = f"{e}"
	return Response(data)

@api_view(["POST"])
def archiveStudent(request):
	data = {}
	if(request.method=='POST'):
		data = request.data['ids']
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
			data["success"] = "Student Archived"
		return Response(data)

@api_view(["POST"])
def removeFromArchiveStudent(request):
	data = {}
	if(request.method=='POST'):
		try:
			data = request.data['ids']
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
				data["success"] = "Student removed from archive"
			return Response(data)
		except Exception as e:
			data["error"] = f"{e}"
	return Response(data)

@api_view(["GET"])
def archiveStudentList(request):
	data = {}
	c_id = request.session['CoachingCentre']
	try:
		center = SignupCoachingCentre.objects.get(s_no=c_id)
	except Exception as e:
		data["error"] = "Coaching Center is not logged In"
		return Response(data)
	data = ArchiveStudents.objects.all()
	print(data)
	serializer = CoachingCenterArchiveStudentDetailSerializer(data,many=True)
	return Response(serializer.data)

@api_view(["PUT"])
def editStudent(request,pk):
	data = {}
	if request.method == "PUT":
		course = AddStudentInst.objects.get(snum=pk)
		serializer = CoachingCenterAddStudentInstSerializer(instance = course, data=request.data)
		if serializer.is_valid():
			serializer.save()
			data["success"] = "Saved Successfully"
			return Response(data)
		data["error"] = "data Couldn't be saved "
		return Response(data)
	

# Add and Save Courses
@api_view(["GET","POST"])
def AddTutorialCenter(request):
	data = {}
	c_id = request.session['CoachingCentre']
	try:
		center = SignupCoachingCentre.objects.get(s_no=c_id)
	except Exception as e:
		data["error"] = e
		return Response(data)
	if request.method == "GET":
		courses = AddCourses.objects.filter(coachingCentre = center)
		tutorials = []
		try:
			for i in courses:
				if TutorialInstitute.objects.filter(Course=i).exists():
					print(TutorialInstitute.objects.filter(Q(Course=i) & Q(Archived=False)))
					tutorials.extend(TutorialInstitute.objects.filter(Q(Course=i) & Q(Archived=False)))
		except:
			tutorials=[]
		serializer = CoachingCenterTutorialInstituteSerializer(tutorials,many=True)
		return Response(serializer.data)

	if request.method == "POST":
		title = request.data['title']
		description = request.data['description']
		fees = request.data['fees']
		duration = request.data.get("duration","")
		course = request.data.get("course","")
		feeDisc = request.data.get("feeDisc","")
		discValidity = request.data.get("discValidity","")
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
		data["success"] = "Course Added Successfully"
		return Response(data)


# Add and Save Courses
@api_view(["POST"])
def AddTutorialCenterVideo(request,pk):
	data = {}
	c_id = request.session['CoachingCentre']
	try:
		center = SignupCoachingCentre.objects.get(s_no=c_id)
	except Exception as e:
		data["error"] = e
		return Response(data)
	tutorial = TutorialInstitute.objects.get(id=pk)
	errors = []
	if request.method == "POST":
		video = request.FILES["video"]
		title = request.data["title"]
		description = request.data["description"]
		try:
			data = TutorialInstitutePlaylist(
				tutorial = tutorial,
				Title = title,
				Description = description,
				Video = video
				)
			data.save()
		except:
			data["error"] = "File Field Cannot be Empty"
			return Response(data)
		data["success"] = "Course Added Successfully"
		return Response(data)

@api_view(["GET","POST"])
def ArchiveTutorialslist(request):
	data = {}
	c_id = request.session['CoachingCentre']
	try:
		center = SignupCoachingCentre.objects.get(s_no=c_id)
	except Exception as e:
		data["error"] = e
		return Response(data)
	if request.method == "GET":
		courses = AddCourses.objects.filter(coachingCentre = center)
		tutorials = []
		for i in courses:
			if TutorialInstitute.objects.filter(Course=i).exists():
				print(TutorialInstitute.objects.filter(Q(Course=i) & Q(Archived=False)))
				tutorials.extend(TutorialInstitute.objects.filter(Q(Course=i) & Q(Archived=True)))

		serializer = CoachingCenterTutorialInstituteSerializer(tutorials,many=True)
		return Response(serializer.data)
	if request.method == "POST":
		ids = request.data['ids']
		if len(ids)<1:
			return Response(data)
		for i in ids:
			if TutorialInstitute.objects.filter(id=i).exists():
				tutorial = TutorialInstitute.objects.get(id=int(i))
				tutorial.Archived = True
				tutorial.save()
				data["success"] = "tutorial Archived Successfully"
		return Response(data)

@api_view(["POST"])
def UnArchiveTutorials(request):
	data = {}
	if request.method == "POST":
		ids = request.data['ids']
		if len(ids)<1:
			data["error"] = "Must provide a list of ids"
			return Response(data)
		for i in ids:
			if TutorialInstitute.objects.filter(id=i).exists():
				tutorial = TutorialInstitute.objects.get(id=int(i))
				tutorial.Archived = False
				tutorial.save()
				data["success"] = "tutorial Archived Successfully"
	return Response(data)


# edit and Delete Tutorials
@api_view(['PUT','DELETE'])
def EditDeleteTutorials(request,pk):
	data = {}
	if request.method == "DELETE":
		fees = TutorialInstitute.objects.get(id=pk)
		fees.delete()
		data["success"] = "Tutorials Deleted Successfully" 
		return Response(data)

	if request.method == "PUT":
		tutorial = TutorialInstitute.objects.get(id=pk)
		title = request.data.get('title',"")
		description = request.data.get('description',"")
		fees = request.data.get('fees',"")
		duration = request.data.get("duration","")
		course = request.data.get("course","")
		feeDisc = request.data.get("feeDisc","")
		discValidity = request.data.get("discValidity","")
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
		data["success"] = "data saved Successfully"
		return Response(data)

@api_view(['POST'])
def WatchTutorialsInstitute(request,course_id):
	data = {}
	c_id = request.session['CoachingCentre']
	try:
		center = SignupCoachingCentre.objects.get(s_no=c_id)
	except Exception as e:
		data["error"] = e
		return Response(data)
	courses = AddCourses.objects.filter(coachingCentre = center)
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
	data = {
	'tutorial':tutorial,
	'start':start,
	'total_length':total_length
	}
	return Response(data)

@api_view(['POST'])
def EditTutorialsInstituteVideos(request,playlist_id):
	data = {}
	tutorial = TutorialInstitutePlaylist.objects.get(id=playlist_id)
	if request.method == "POST":
		video = request.data.get('video','')
		title = request.data.get('title',"")
		description = request.data.get('description',"")
		if title:
			tutorial.Title = title
		if description:
			tutorial.Description = description
		if video:
			tutorial.Video = video
		tutorial.save()
		data["Success"] = "data Saved successfully"
	return Response(data)

@api_view(['POST'])
def DeleteTutorialsInstituteVideos(request,playlist_id):
	data = {}
	tutorial = TutorialInstitutePlaylist.objects.get(id=playlist_id)
	tutorial.delete()
	data["success"] = "data deleted successfully"
	return Response(data)

@api_view(['POST'])
def AddExamInstitute(request):
	data = {}
	c_id = request.session['CoachingCentre']
	try:
		center = SignupCoachingCentre.objects.get(s_no=c_id)
	except Exception as e:
		data["error"] = e
		return Response(data)
	if request.method == "POST":
		course = request.data.get('course','')
		course = AddCourses.objects.get(s_num=course)
		classes = request.data.get('class','')
		Batch = request.data.get('batch','')
		name = request.data.get('examname','')
		date = request.data.get('date','')
		date = datetime.strptime(date, "%Y-%m-%d")
		exam_time = request.data.get('exam_time','')
		timezone_offset = request.data.get('timezone_offset','')
		duration = request.data.get('duration','')
		pp = request.data.get('pp','')
		redate = request.data.get('redate','')
		calculator = request.data.get('calculator','')
		imguplod = request.data.get('imguplod','')
		nm = request.data.get('nm','')
		negative_marks = request.data.get('negative_marks','')
		tc = request.data.get('tc','')
		status = request.data.get('status','')
		noquestions = request.data.get('noquestions','')
		data = Exam()
		data.center = center
		data.course = course
		data.Class = classes
		data.Batch = Batch
		data.Name = name
		data.exam_date = date
		Time = exam_time.split(':')
		d = dt.time(int(Time[0]),int(Time[1]),00)
		data.exam_time = d
		data.exam_duration = duration
		data.timezone = timezone_offset
		data.pass_percentage = pp
		if redate:
			data.reexam_date = redate
		if calculator:
			data.calculator = True
		if imguplod:
			data.imgupload = True
		if nm:
			data.negative_marking = True
			data.negative_marks = negative_marks
		data.tandc = tc
		if status==1:
			data.status = True
		else:
			data.status = False
		data.question_count = noquestions
		data.save()
		data["success"] = "data Saved successfully"
	return Response(data)

@api_view(['GET'])
def ListExams(request):
	data = {}
	c_id = request.session['CoachingCentre']
	try:
		center = SignupCoachingCentre.objects.get(s_no=c_id)
	except Exception as e:
		data["error"] = e
		return Response(data)
	context = {}
	if Exam.objects.filter(center=center).exists():
		exams = Exam.objects.filter(center=center)
		serializer = CoachingCenterExamSerializer(exams,many=True)
	return Response(serializer.data)

@api_view(['POST'])
def ToggleExam(request,exam_id):
	data = {}
	exam = Exam.objects.get(id=exam_id)
	if exam.status == True:
		exam.status = False
		data["success"] = "Exam Deactivated"
	else:
		exam.status = True
		data["success"] = "Exam Activated"
	exam.save()
	return Response(data)

@api_view(['POST'])
def Editexam(request,exam_id):
	data = {}
	exam = Exam.objects.get(id=exam_id)
	if request.method == "POST":
		course = request.data.get('course','')
		classes = request.data.get('class','')
		Batch = request.data.get('batch','')
		name = request.data.get('examname','')
		date = request.data.get('date','')
		exam_time = request.data.get('exam_time','')
		timezone_offset = request.data.get('timezone_offset','')
		duration = request.data.get('duration','')
		pp = request.data.get('pp','')
		redate = request.data.get('redate','')
		calculator = request.data.get('calculator','')
		imguplod = request.data.get('imguplod','')
		nm = request.data.get('nm','')
		negative_marks = request.data.get('negative_marks','')
		tc = request.data.get('tc','')
		status = request.data.get('status','')
		noquestions = request.data.get('noquestions','')
		if course:
			course = AddCourses.objects.get(s_num=course)
			exam.course = course
		if classes:
			exam.Class = classes
		if Batch:
			exam.Batch = Batch
		if name:
			exam.Name = name
		if date:
			date = datetime.strptime(date, "%Y-%m-%d")
			exam.exam_date = date
		if exam_time:
			Time = exam_time.split(':')
			d = dt.time(int(Time[0]),int(Time[1]),00)
			exam.exam_time = d
		if duration:
			exam.exam_duration = duration
		if timezone_offset:
			exam.timezone = timezone_offset
		if pp:
			exam.pass_percentage = pp
		if redate:
			exam.reexam_date = redate
		if calculator:
			exam.calculator = True
		if imguplod:
			exam.imgupload = True
		if nm:
			exam.negative_marking = True
			exam.negative_marks = negative_marks
		exam.tandc = tc
		if status==1:
			exam.status = True
		else:
			exam.status = False
		exam.question_count = noquestions
		exam.save()
		data["Success"] = "data Saved Successfully"
	return Response(data)

@api_view(['DELETE'])
def deleteExam(request,exam_id):
	exam = Exam.objects.get(id=exam_id)
	exam.delete()
	data["Success"] = "data Deleted Successfully"
	return Response(data)


@api_view(['GET'])
def SearchExam(request,search):
	data = {}
	c_id = request.session['CoachingCentre']
	try:
		center = SignupCoachingCentre.objects.get(s_no=c_id)
	except Exception as e:
		data["error"] = e
		return Response(data)
	context = {}
	if Exam.objects.filter(center=center).exists():
		exams = Exam.objects.filter(Q(center=center))
		exams = exams.filter(Q(Name__icontains = search) | Q(course__courseName__icontains = search))
		serializer = CoachingCenterExamSerializer(exams,many=True)
	return Response(serializer.data)


@api_view(['POST'])
def AddNotesInstitute(request):
	data = {}
	c_id = request.session['CoachingCentre']
	try:
		center = SignupCoachingCentre.objects.get(s_no=c_id)
	except Exception as e:
		data["error"] = e
		return Response(data)
	if request.method == "POST":
		note = request.FILES.get("note","")
		title = request.data.get("title","")
		description = request.data.get("description","")
		course = request.data.get("course","")
		if (note and title and description and course):
			data = NotesInstitute(
				center = center,
				notes = note,
				title = title,
				subject = course,
				description = description,
				)
			try:
				data.save()
				data["Success"] = "data Saved Successfully"
				return Response(data)
			except:
				data["error"] = "error occured"
				return Response(data)

@api_view(['GET'])
def ViewNotesInstitute(request):
	data = {}
	c_id = request.session['CoachingCentre']
	try:
		center = SignupCoachingCentre.objects.get(s_no=c_id)
	except Exception as e:
		data["error"] = e
		return Response(data)
	notes = NotesInstitute.objects.filter(center=center)
	serializer = CoachingCenterNotesSerializer(notes,many=True)
	return Response(serializer.data)

@api_view(['GET'])
def PdfViewNoteInstitute(request,note_id):
	note = NotesInstitute.objects.get(id=note_id)
	serializer = CoachingCenterNotesSerializer(note,many=False)
	return Response(serializer.data)

@api_view(['POST'])
def EditNoteInstitute(request,note_id):
	if request.method == "POST":
		data = NotesInstitute.objects.get(id=note_id)
		note = request.FILES.get("note","")
		title = request.data.get("title","")
		description = request.data.get("description","")
		course = request.data.get("course","")
		if note:
			data.notes = note
		if title:
			data.title = title
		if description:
			data.description = description
		if course:
			data.subject = course
		try:
			data.save()
			data["Success"] = "data Saved Successfully"
			return Response(data)
		except:
			data["error"] = "error occured"
			return Response(data)

@api_view(['POST'])
def DeleteNoteInstitute(request,note_id):
	note = NotesInstitute.objects.get(id=note_id)
	note.delete()
	data["Success"] = "data Deleted Successfully"
	return Response(data)


@api_view(['GET'])
def SearchNotes(request,search):
	data = {}
	c_id = request.session['CoachingCentre']
	try:
		center = SignupCoachingCentre.objects.get(s_no=c_id)
	except Exception as e:
		data["error"] = e
		return Response(data)
	if NotesInstitute.objects.filter(center=center).exists():
		notes = NotesInstitute.objects.filter(Q(center=center))
		exams = notes.filter(Q(notes__icontains = search) | Q(title__icontains = search) | Q(subject__icontains = search))
		serializer = CoachingCenterNotesSerializer(exams,many=True)
	return Response(serializer.data)


# Center Result Section
@api_view(['GET'])
def CoachingResult(request):
	data = {}
	c_id = request.session['CoachingCentre']
	try:
		center = SignupCoachingCentre.objects.get(s_no=c_id)
	except Exception as e:
		data["error"] = e
		return Response(data)
	if Exam.objects.filter(center=center).exists():
		exams = Exam.objects.filter(Q(center=center))
		serializer = CoachingCenterExamSerializer(exams,many=True)
		return Response(serializer.data)

@api_view(['GET'])
def GetExamResults(request,exam_id):
	exam = Exam.objects.get(id=exam_id)
	students = StudentMapping.objects.filter(exam=exam)
	serializer = SignupStudentSerializer(students,many=True)
	return Response(serializer.data)

@api_view(['GET'])
def GetStudentResults(request,student_id,exam_id):
	data = {}
	mapping = StudentMapping.objects.get(id=student_id)
	student = SignupStudentSerializer(mapping,many=False)

	exam = Exam.objects.get(id=exam_id)
	Ex = CoachingCenterExamSerializer(exam,many=False)

	status = StudentExamResult.objects.get(student=mapping,exam=exam)
	status = SignupStudentExamResultSerializer(status,many=True)

	student_results = StudentAnswer.objects.filter(student=mapping,exam=exam)
	serializer = SignupStudentExamAnswersSerializer(student_results,many=True)

	data = {
	'student_results':serializer,
	'student':status,
	'exam':Ex,
	'mapping':student
	}
	return Response(serializer.data)
	
@api_view(["POST"])
def CreateQuestionsCenter(request,exam_id):
	data = {}
	exam = Exam.objects.get(id=exam_id)
	if request.method=="POST":
		question_type = request.data.get('question_type',"")
		question = request.data.get('question',"")
		solution = request.data.get('solution',"")
		marks = request.data.get('marks',"")
		section = request.data.get('section',"")
		negative_marks = request.data.get('negative_marks',"")
		hindi = request.data.get("hinditext","")
		if hindi:
			question=hindi
		if question_type=='sq':
			try:
				data = ShortAnswerQuestion(
					exam=exam,
					question=question,
					correct_ans=solution,
					marks=marks,
					section=section)
				if negative_marks:
					data.negative_marks=negative_marks
				else:
					data.negative_marks=0.0
				data.save()
			except:
				data["error"] = 'Options Cannot be Empty'
				return Response(data)
		elif question_type=='lq':
			try:

				data = LongAnswerQuestion(
					exam=exam,
					question=question,
					correct_ans=solution,
					marks=marks,
					section=section)
				if negative_marks:
					data.negative_marks=negative_marks
				else:
					data.negative_marks=0.0
				data.save()
			except:
				data["error"] = 'Options Cannot be Empty'
				return Response(data)
		elif question_type=='mc':
			try:

				options = request.data['options']
				print(options)
				data = MultipleQuestion(
					exam=exam,
					question=question,
					correct_ans=solution,
					marks=marks,
					section=section
					)
				if negative_marks:
					data.negative_marks=negative_marks
				else:
					data.negative_marks=0.0
				data.save()
			except:
				data["error"] = 'Options Cannot be Empty'
				return Response(data)
			if options:
				for option in options:
					answer = MultipleAnswer(
						question = MultipleQuestion.objects.get(id=data.id),
						option = option
						)
					answer.save()
			else:
				data["error"] = 'Options Cannot be Empty'
				return Response(data)
		else:
			try:
				options = request.data['options']
				print(options)
				bexam = BooleanQuestion(
					exam=exam,
					question=question,
					option1 = options[0],
					option2 = options[1],
					correct_ans=solution,
					marks=marks,
					section=section)
				if negative_marks:
					bexam.negative_marks=negative_marks
				else:
					bexam.negative_marks=0.0
				bexam.save()
			except Exception as e:
				data["error"] = 'e'
				return Response(data)
		data["success"] = "data Saved Successfully"
		return Response(data)

def QuestionsResponse(exam_id):	
		shortquestions = ShortAnswerQuestion.objects.filter(exam=exam_id)
		booleanquestions = BooleanQuestion.objects.filter(exam=exam_id)
		longquestions = LongAnswerQuestion.objects.filter(exam=exam_id)
		multiplequestions = MultipleQuestion.objects.filter(exam=exam_id)
		x=1
		for i in ['A','B','C','D']:
			query1,query2,query3,query4=[],[],[],[]
			query1 = shortquestions.filter(section=i)
			query2 = booleanquestions.filter(section=i)
			query3 = longquestions.filter(section=i)
			query4 = multiplequestions.filter(section=i)
			for item in query1:
				item.question_no = x
				item.save()
				x+=1
			for item in query2:
				item.question_no = x
				item.save()
				x+=1
			for item in query3:
				item.question_no = x
				item.save()
				x+=1
			for item in query4:
				item.question_no = x
				item.save()
				x+=1

@api_view(["POST"])
def profileCoachingCentre(request):
	data = {}
	c_id = request.session['CoachingCentre']
	try:
		currentCC = SignupCoachingCentre.objects.get(s_no=c_id)
	except Exception as e:
		data["error"] = e
		return Response(data)
	if(request.method=='POST'):
		if 'otpReceived' in request.POST:
			otp = request.data.get('otp')
			email = request.data.get('email')
			otp_obj = OTP.obects.get(type='any',user=email)
			if (currentCC.email==email) and otp_obj:
				if otp_obj.otp==otp:
					currentCC.emailValidated = True
					currentCC.save()
			otp_obj.delete()
			data["success"] = "Otp verified Successfully"
			return Response(data)
		else:
			instName = request.data.get('instituteName')
			phone = request.data.get('phone')
			oldPassword = request.data.get('oldPassword')
			newPassword = request.data.get('newPassword')
			confPassword = request.data.get('confirmPassword')
			latitude = request.data.get('cityLat')
			longitude = request.data.get('cityLng')
			loaction = request.data.get('loc')
			image = request.FILES.get('photo')
			showFees = request.data.get('showFees')
			print('image',image)
			error = 0
			if(not phone.isdigit()):
				data["success"] = "Phone number should be numeric."
				return Response(data)
			if(len(phone)!=10):
				data["success"] = "Phone number should be 10 digits long."
				return Response(data)
			if(len(newPassword)<3 or len(newPassword)>20):
				data["success"] = "Password length should be between 3 and 20"
				return Response(data)
			if(oldPassword!=currentCC.password):
				data["success"] = "Enter you correct old password."
				return Response(data)
			if(newPassword!=confPassword):
				data["success"] = "New Password and Confirm Password donot match"
				return Response(data)
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
			data["Success"] = "data saved successfully"
			return Response(data)

@api_view(["GET"])
def QuestionsCenter(request,exam_id):
	QuestionsResponse(exam_id)
	shortquestions = ShortAnswerQuestion.objects.filter(exam=exam_id)
	booleanquestions = BooleanQuestion.objects.filter(exam=exam_id)
	longquestions = LongAnswerQuestion.objects.filter(exam=exam_id)
	multiplequestions = MultipleQuestion.objects.filter(exam=exam_id)
	short =  SignupStudentShortAnswerQuestionSerializer(shortquestions,many=True)
	boolean = SignupStudentBooleanAnswerQuestionSerializer(booleanquestions,many=True)
	long = SignupStudentLongAnswerQuestionSerializer(longquestions,many=True)
	multiple = SignupStudentMultipleAnswerQuestionSerializer(multiplequestions,many=True)

	data = list(chain(short.data,boolean.data))
	data.extend(long.data)
	data.extend(multiple.data)
	data.sort(key=lambda x:x['question_no'])
	print(data)
	return Response(data)


###################################### Tutor Api's#######################################

@api_view(["GET"])
def enrolledStudents(request):
	if(request.method=='GET'):
		searchQuery = Q(budget__gte=0)
		className = request.data['className']
		courceName = request.data['courseName']
		la1 = float(request.data.get('cityLat'))
		lo1 = float(request.data.get('cityLng'))
		if(courceName):
			print(courceName)
			searchQuery &= Q(courseName=courceName)
		if(className):
			searchQuery &= Q(forclass=className)
		if(budgetVal):
			searchQuery &= Q(budget__lte=budgetVal)
		initialdata = PostTution.objects.filter(searchQuery)
		finaldata = []
		for x in initialdata:
			la2 = float(x.connector.latitude)
			lo2 = float(x.connector.longitude)
			distance = distanceBwAB((la1,lo1),(la2,lo2)).km
			if(float(tutorObj.distance)<=float(distance)):
				finaldata.append(x)
		serializer = SignupStudentPostTuitionSerializer(finaldata,many=True)
		return Response(serializer.data)

@api_view(["GET"])
def viewAssignmentTutor(request):
	if request.method=='GET':
		searchQuery = Q(budget__gte=0)
		className = request.POST.get('className')
		courceName = request.POST.get('courseName')
		budgetVal = request.POST.get('budget')
		la1 = request.POST.get('cityLat',"")
		lo1 = request.POST.get('cityLng',"")
		print(la1,lo1)
		if(courceName):
			searchQuery &= Q(courseName=courceName)
		if(className):
			searchQuery &= Q(forclass=className)
		if(budgetVal):
			searchQuery &= Q(budget__lte=budgetVal)
		initialdata = PostAssignment.objects.filter(searchQuery)
		if la1 and lo1 and initialdata:
			finaldata = []
			for x in initialdata:
				la2 = float(x.connector.latitude)
				lo2 = float(x.connector.longitude)
				distance = distanceBwAB((float(la1),float(lo1)),(la2,lo2)).km
				if(float(tutorObj.distance)<=float(distance)):
					finaldata.append(x)
		serializer = SignupStudentPostAssignmentSerializer(finaldata,many=True)
		return Response(serializer.data)



# Tutorial Tutor
# Add and get Courses
@api_view(["GET","POST"])
def AddTutorialTutor(request):
	data = {}
	sno = request.session['Tutor']
	try:
		tutor = SignupTutor.objects.get(sno = sno)
	except Exception as e:
		data["error"] = e
		return Response(data)
	if request.method == "GET":
		tutorials = TutorialTutors.objects.filter(Q(Tutor=tutor) & Q(Archived=False))
		serializer = TutorAddTutorialSerializer(tutorials,many=True)
		return Response(serializer.data)

	if request.method == "POST":
		title = request.data['title']
		description = request.data['description']
		fees = request.data['fees']
		duration = request.data.get("duration","")
		course = request.data.get("course","")
		feeDisc = request.data.get("feeDisc","")
		discValidity = request.data.get("discValidity","")
		discValidity = datetime.strptime(discValidity,'%Y-%m-%d')
		print(title,description,fees,duration,course,feeDisc,discValidity)
		tutorial = TutorialTutors(
			Title = title,
			Tutor = tutor,
			Fees = fees,
			Duration = duration,
			Description = description,
			Validity = discValidity,
			Discount = feeDisc,
			)
		tutorial.save()
		data["success"] = "Course Added Successfully"
		return Response(data)


# Add and Save Courses
@api_view(["POST"])
def AddTutorialTutorVideo(request,pk):
	data = {}
	sno = request.session['Tutor']
	try:
		tutor = SignupTutor.objects.get(sno = sno)
	except Exception as e:
		data["error"] = e
		return Response(data)
	tutorial = TutorialTutors.objects.get(id=pk)
	if request.method == "POST":
		video = request.FILES["video"]
		title = request.data["title"]
		description = request.data["description"]
		try:
			tutoria = TutorialTutorsPlaylist(
				tutorial = tutorial,
				Title = title[item],
				Description = description[item],
				Video = video[item])
			tutoria.save()
		except:
			data["error"] = "File Field Cannot be Empty"
			return Response(data)
		data["success"] = "Course Added Successfully"
		return Response(data)

@api_view(["GET","POST"])
def ArchiveTutorialstutorlist(request):
	data = {}
	sno = request.session['Tutor']
	try:
		tutor = SignupTutor.objects.get(sno = sno)
	except Exception as e:
		data["error"] = e
		return Response(data)
	if request.method == "GET":
		tutorials = TutorialTutors.objects.filter(Q(Tutor=tutor) & Q(Archived=True))
		serializer = TutorAddTutorialSerializer(tutorials,many=True)
		return Response(serializer.data)
	
	if request.method == "POST":
		ids = request.data['ids']
		if len(ids)<1:
			data["error"] = "must provide List of Id"
			return Response(data)
		for i in ids:
			if TutorialTutors.objects.filter(id=i).exists():
				tutorial = TutorialTutors.objects.get(id=int(i))
				tutorial.Archived = False
				tutorial.save()
				data["success"] = "tutorial Unarchived Successfully"
		return Response(data)

@api_view(["POST"])
def ArchiveTutorialstutor(request):
	data = {}
	if request.method == "POST":
		ids = request.data['ids']
		if len(ids)<1:
			data["error"] = "Must provide a list of ids"
			return Response(data)
		for i in ids:
			if TutorialTutors.objects.filter(id=i).exists():
				tutorial = TutorialTutors.objects.get(id=int(i))
				tutorial.Archived = False
				tutorial.save()
				data["success"] = "tutorial Archived Successfully"
	return Response(data)


# edit and Delete Tutorials
@api_view(['PUT','DELETE'])
def EditDeleteTutorialstutor(request,pk):
	data = {}
	if request.method == "DELETE":
		data = TutorialTutors.objects.get(id=pk)
		data.delete()
		data["success"] = "Tutorials Deleted Successfully" 
		return Response(data)

	if request.method == "PUT":
		tutorial = TutorialTutors.objects.get(id=pk)
		title = request.data.get('title',"")
		description = request.data.get('description',"")
		fees = request.data.get('fees',"")
		duration = request.data.get("duration","")
		course = request.data.get("course","")
		feeDisc = request.data.get("feeDisc","")
		discValidity = request.data.get("discValidity","")
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
		data["success"] = "data saved Successfully"
		return Response(data)

@api_view(['POST'])
def WatchTutorialsTutor(request,course_id):
	data = {}
	sno = request.session['Tutor']
	try:
		tutor = SignupTutor.objects.get(sno = sno)
	except Exception as e:
		data["error"] = e
		return Response(data)
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
	return Response(data)

@api_view(['POST'])
def EditTutorialsTutorVideos(request,playlist_id):
	data = {}
	tutorial = TutorialTutorsPlaylist.objects.get(id=playlist_id)
	if request.method == "POST":
		video = request.data.get('video','')
		title = request.data.get('title',"")
		description = request.data.get('description',"")
		if title:
			tutorial.Title = title
		if description:
			tutorial.Description = description
		if video:
			tutorial.Video = video
		tutorial.save()
		data["Success"] = "data Saved successfully"
	return Response(data)

@api_view(['POST'])
def DeleteTutorialsTutorVideos(request,playlist_id):
	data = {}
	tutorial = TutorialTutorsPlaylist.objects.get(id=playlist_id)
	tutorial.delete()
	data["success"] = "data deleted successfully"
	return Response(data)

@api_view(["POST","GET"])
def AddBatchTutor(request):
	data = {}
	sno = request.session['Tutor']
	try:
		tutor = SignupTutor.objects.get(sno = sno)
	except Exception as e:
		data["error"] = e
		return Response(data)
	if request.method == "GET":
		tutorials = BatchTimingTutor.objects.filter(Tutor=tutor)
		serializer = TutorBatchTimingSerializer(tutorials,many=True)
		return Response(serializer.data)

	if request.method == "PUT":
		name = request.data["Name"]
		starttime = request.data['starttime']
		endtime = request.data['endtime']
		startdate = request.data['startdate']
		enddate = request.data['enddate']
		noofdays = request.data['days']
		noofdays = ",".join(noofdays)
		startdate = datetime.strptime(startdate,'%Y-%m-%d')
		enddate = datetime.strptime(enddate,'%Y-%m-%d')
		batch = BatchTimingTutor(
			batchName = name,
			days = noofdays,
			startTime = starttime,
			endTime = endtime,
			StartDate = startdate,
			EndDate = enddate,
			Tutor = tutor,
			)
		batch.save()
		data["success"] = "data Saved successfully"
		return Response(data)

@api_view(["POST"])
def SearchTutorialsTutor(request):
	srch = request.data['search']
	match = TutorialTutors.objects.filter(Q(Title__icontains=srch)| 
		Q(Description__icontains=srch))
	serializer = TutorAddTutorialSerializer(match,many=True)
	return Response(serializer.data)


@api_view(['POST',"GET"])
def AddNotesTutor(request):
	data = {}
	sno = request.session['Tutor']
	try:
		tutor = SignupTutor.objects.get(sno = sno)
	except Exception as e:
		data["error"] = e
		return Response(data)
	if request.method == "GET":
		notes = NotesTutor.objects.filter(tutor=tutor)
		serializer = TutorAddNoteSerializer(notes,many=True)
		return Response(serializer.data)
	
	if request.method == "POST":
		note = request.FILES.get("note","")
		title = request.data.get("title","")
		description = request.data.get("description","")
		course = request.data.get("course","")
		if (note and title and description and course):
			data = NotesTutor(
				tutor = tutor,
				notes = note,
				title = title,
				subject = course,
				description = description,
				)
			try:
				data.save()
				data["Success"] = "data Saved Successfully"
				return Response(data)
			except:
				data["error"] = "error occured"
				return Response(data)


@api_view(['PUT',"DELETE"])
def EditNoteTutor(request,note_id):
	data = {}
	if request.method == "DELETE":
		note = NotesTutor.objects.get(id=note_id)
		note.delete()
		data["success"] = "data deleted successfully"
		return Response(data)

	if request.method == "PUT":
		data = NotesTutor.objects.get(id=note_id)
		note = request.FILES.get("note","")
		title = request.data.get("title","")
		description = request.data.get("description","")
		course = request.data.get("course","")
		if note:
			data.notes = note
		if title:
			data.title = title
		if description:
			data.description = description
		if course:
			data.subject = course
		try:
			data.save()
			data["Success"] = "data Saved Successfully"
			return Response(data)
		except:
			data["error"] = "error occured"
			return Response(data)

@api_view(['GET'])
def PdfViewNoteTutor(request,note_id):
	note = NotesTutor.objects.get(id=note_id)
	serializer = TutorAddNoteSerializer(note,many=False)
	return Response(serializer.data)


@api_view(['GET'])
def SearchNotesTutor(request,search):
	data = {}
	sno = request.session['Tutor']
	try:
		tutor = SignupTutor.objects.get(sno = sno)
	except Exception as e:
		data["error"] = e
		return Response(data)
	if NotesTutor.objects.filter(center=center).exists():
		notes = NotesTutor.objects.filter(Q(center=center))
		exams = notes.filter(Q(description__icontains = search) | Q(title__icontains = search) | Q(subject__icontains = search))
		serializer = CoachingCenterNotesSerializer(exams,many=True)
	return Response(serializer.data)

@api_view(['POST'])
def profileTutor(request):
	data = {}
	sno = request.session['Tutor']
	try:
		tutorObj = SignupTutor.objects.get(sno = sno)
	except Exception as e:
		data["error"] = e
		return Response(data)
	l = len(tutorObj.signupTutorContinued.all())
	try:
		signupTutContObj = tutorObj.signupTutorContinued.all()[l-1]
	except Exception as e:
		print(e)
	if(request.method=='POST'):
		if 'otpReceived' in request.data:
			otp = request.data.get('otp')
			email = request.data.get('email')
			otp_obj = OTP.obects.get(type='any',user=email)
			if (tutorObj.email==email) and otp_obj:
				if otp_obj.otp==otp:
					tutorObj.emailValidated = True
					tutorObj.save()
					data["success"] = "Email Validated"
			otp_obj.delete()
			return Response(data)
		else:
			firstName = request.data.get('firstName')
			lastName = request.data.get('lastName')
			phone = request.data.get('phone')
			oldPassword = request.data.get('oldPassword')
			newPassword = request.data.get('newPassword')
			confPassword = request.data.get('confirmPassword')
			location = request.data.get('loc')
			availability = ', '.join(request.data.getlist('availability'))
			qualification = request.data.get('qualification')
			experience = request.data.get('experience')
			description = request.data.get('description')
			freeDemo = request.data.get('fda')
			image = request.data.get('photo')
			distance = request.data.get('distance',0)
			gender = request.data.get('gender','A')
			fees  = request.data.get('fees',0)
			latitude = request.data.get('cityLat')
			longitude = request.data.get('cityLng')
			error = 0
			if(not phone.isdigit()):
				data["error"] = "Phone number should be numeric."
				return Response(data)
			if(len(phone)!=10):
				data["error"] = "Phone number should be 10 digits long."
				return Response(data)
			if(len(newPassword)<3 or len(newPassword)>20):
				data["error"] = "Password length should be between 3 and 20"
				return Response(data)
			if(oldPassword!=tutorObj.password):
				data["error"] = "Enter you correct old password."
				return Response(data)
			if(newPassword!=confPassword):
				data["error"] = "New Password and Confirm Password donot match"
				return Response(data)

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
		data["succes"] = "data Have Been Saved Successfully"
		return Response(data)

@api_view(['POST'])
def loginTutor(request):
	data = {}
	if request.method=="POST":
		username = request.data.get('username', '')
		password1 = request.data.get('password1', '')
		inst_names = SignupTutor.objects.values('username', 'password','sno')
		rememberMe = request.data.get('remember',False)
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
					data["succes"] = "User Logged In Successfully"
					return Response(data)
				else:
					data["redirect"] = "To Continue"
					return Response(data)
		data["error"] = "Invalid Credentials, Please try again"
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
					data["succes"] = "User Logged In Successfully"
					responce = Response(data)
					responce.set_cookie('TutorName',item['username'],max_age=max_age)
					responce.set_cookie('TutorAvatar',SignupTutor.objects.get(username=username,password=password1,sno=item['sno']).signupTutorContinued.all()[len(subDetails)-1].avatar,max_age=max_age)
					responce.set_cookie('TutorPhoto',SignupTutor.objects.get(username=username,password=password1,sno=item['sno']).signupTutorContinued.all()[len(subDetails)-1].photo,max_age=max_age)
					return responce
				else:
					data["redirect"] = "To Continue"
					responce = Response(data)
					responce.set_cookie('TutorName',item['username'],max_age=max_age)
					return responce
			except ValueError:
				data["error"] = "Invalid Credentials, Please try again"
				return Response(data)
	return Response(data)

@api_view(['POST'])
def signupTutor(request):
	errors = []
	prefil = {}
	if request.method=="POST":
		firstName = request.data.get('firstName', '')
		count= SignupTutor.objects.all().count()
		count=count+1
		name= request.data.get('firstName', '')
		ch1=str("%04d" % count)
		ch2=str(name[0:2])
		tutorCode=ch2+ch1
		lastName = request.data.get('lastName', '')
		email = request.data.get('email', '')
		username = email
		password = request.data.get('password', '')
		distance = request.data.get('distance','')
		latitude = request.data.get('cityLat')
		longitude = request.data.get('cityLng')
		phone = request.data.get('phone', '')
		location = request.data.get('loc', '')
		prefil = {
			"username":username,
			"firstName":firstName,
			"lastName":lastName,
			"email":email,
			"distance":distance,
			"phone":phone,
		}

		if firstName.isalpha() == False | lastName.isalpha() == False:
			data["error"] = "Name must be alphabetical"
			return Response(data)
		if len(phone) != 10:
			data["error"] = "Phone Number must be 10 digits"
			return Response(data)
		if phone.isdigit() == False:
			data["error"] = "Phone number should be numeric."
			return Response(data)			
		if distance.isdigit() == False:
			data["error"] = "Distance must be numeric"
			return Response(data)			
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
			data["success"] = "User Saved Successfully"
			return Response(data)

@api_view(['POST'])	
def signupTutorContinued(request,sno):
	if(request.method=='POST'):
		baseModel = SignupTutor.objects.get(sno=sno)
		# creating data object
		forclass = request.data.get('cn_combined')
		forclass = ";".join(forclass)
		courseName = request.data.get('ctn_combined')
		courseName = ";".join(courseName)
		availability = request.data.get('availability')
		availability = ", ".join(availability)
		image = request.data.get('photo')
		obj = SignupTutorContinued(
				base            = baseModel,
				availability    = request.data.getlist('availability'),
				qualification   = request.data.get('qualification'),
				description     = request.data.get('description'),
				experience      = request.data.get('experience'),
				gender          = request.data.get('gender'),
				courseName      = courseName,
				forclass        = forclass,
				fees            = float(request.data.get('fees',1.1)),
				freeDemo        = request.data.get('fda',0)
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
		data["success"] = "User Saved Successfully"
		responce = Response(data)
		responce.set_cookie('TutorAvatar',obj.avatar)
		responce.set_cookie('TutorPhoto',obj.photo)
		return responce

@api_view(['POST',"GET"])
def ExamTutor(request):
	result = {}
	sno = request.session['Tutor']
	try:
		tutor = SignupTutor.objects.get(sno = sno)
	except Exception as e:
		result["error"] = e
		return Response(result)

	if enrollTutors.objects.filter(signUp=tutor).exists():
		tutors = enrollTutors.objects.filter(signUp=tutor)
		institute = AddTutorsInst.objects.get(username=tutors.first())
		print(institute.cid)

		if request.method == "GET":
			exams = Exam.objects.filter(center=institute.cid)
			serializer = CoachingCenterExamSerializer(exams,many=True)
			return Response(serializer.data)

		if request.method == "POST":
			course = request.data.get('course','')
			course = AddCourses.objects.get(s_num=course)
			classes = request.data.get('class','')
			Batch = request.data.get('batch','')
			name = request.data.get('examname','')
			date = request.data.get('date','')
			date = datetime.strptime(date, "%Y-%m-%d")
			exam_time = request.data.get('exam_time','')
			timezone_offset = request.data.get('timezone_offset','')
			duration = request.data.get('duration','')
			pp = request.data.get('pp','')
			redate = request.data.get('redate','')
			calculator = request.data.get('calculator','')
			imguplod = request.data.get('imguplod','')
			nm = request.data.get('nm','')
			negative_marks = request.data.get('negative_marks','')
			tc = request.data.get('tc','')
			status = request.data.get('status','')
			noquestions = request.data.get('noquestions','')
			data = Exam()
			data.center = institute.cid
			data.course = course
			data.Class = classes
			data.Batch = Batch
			data.Name = name
			data.exam_date = date
			Time = exam_time.split(':')
			d = dt.time(int(Time[0]),int(Time[1]),00)
			data.exam_time = d
			data.exam_duration = duration
			data.timezone = timezone_offset
			data.pass_percentage = pp
			if redate:
				data.reexam_date = redate
			if calculator:
				data.calculator = True
			if imguplod:
				data.imgupload = True
			if nm:
				data.negative_marking = True
				data.negative_marks = negative_marks
			data.tandc = tc
			if status==1:
				data.status = True
			else:
				data.status = False
			data.question_count = noquestions
			data.save()
			result["success"] = "data Saved successfully"
			return Response(result)
	else:
		result["error"] = "Tutor is not Enrolled in Institute"
		return Response(result)

@api_view(['POST'])
def EditShortQuestionsTutor(request,question_id):
	data = {}
	try:
		question = ShortAnswerQuestion.objects.get(id=question_id)
	except:
		data["error"] = 'Error Processing Request!'
		return Response(data)
	if request.method == "POST":
		section = request.data.get("section","")
		marks = request.data.get("marks","")
		nm= request.data.get("nm","")
		negative_marks = request.data.get("negative_marks","")
		Question = request.data.get("question","")
		Solution = request.data.get("solution","")
		#print(section,marks,nm,negative_marks,question,solution)
		if section:
			question.section = section
		if marks:
			question.marks = marks
		if nm:
			question.negative_marks=negative_marks
		if Question:
			question.question=Question
		if Solution:
			question.correct_ans=Solution
		try:
			question.save()
			data["success"] = 'Question Saved Successfully'
		except:
			data["error"] = 'Error Processing Request!'
			return Response(data)
		return Response(data)

@api_view(['POST'])
def EditLongQuestionsTutor(request,question_id):
	data = {}
	try:
		question = LongAnswerQuestion.objects.get(id=question_id)
	except:
		data["error"] = 'Error Processing Request!'
		return Response(data)
	if request.method == "POST":
		section = request.data.get("section","")
		marks = request.data.get("marks","")
		nm= request.data.get("nm","")
		negative_marks = request.data.get("negative_marks","")
		Question = request.data.get("question","")
		Solution = request.data.get("solution","")
		if section:
			question.section = section
		if marks:
			question.marks = marks
		if nm:
			question.negative_marks=negative_marks
		if Question:
			question.question=Question
		if Solution:
			question.correct_ans=Solution
		try:
			question.save()
			data["success"] = 'Question Saved Successfully'
		except:
			data["error"] = 'Error Processing Request!'
			return Response(data)
		return Response(data)

@api_view(['POST'])
def EditBooleanQuestionsTutor(request,question_id):
	data = {}
	try:
		question = BooleanQuestion.objects.get(id=question_id)
	except:
		data["error"] = 'Error Processing Request!'
		return Response(data)

	if request.method == "POST":
		section = request.data.get("section","")
		marks = request.data.get("marks","")
		nm= request.data.get("nm","")
		negative_marks = request.data.get("negative_marks","")
		Question = request.data.get("question","")
		Solution = request.data.get("solution","")
		option1 = request.data.get("option1","")
		option2 = request.data.get("option2","")
		#print(section,marks,nm,negative_marks,question,solution)
		if section:
			question.section = section
		if marks:
			question.marks = marks
		if nm:
			question.negative_marks=negative_marks
		if Question:
			question.question=Question
		if Solution:
			question.correct_ans=Solution
		if option1:
			question.option1=option1
		if option2:
			question.option2 = option2
		try:
			question.save()
			data["success"] = 'Question Saved Successfully'
		except:
			data["error"] = 'Error Processing Request!'
			return Response(data)
		return Response(data)

@api_view(['POST'])
def EditMultipleQuestionsTutor(request,question_id):
	errors =[]
	try:
		question = MultipleQuestion.objects.get(id=question_id)
	except:
		data["error"] = 'Error Processing Request!'
		return Response(data)
	if request.method == "POST":
		section = request.data.get("section","")
		marks = request.data.get("marks","")
		nm= request.data.get("nm","")
		negative_marks = request.data.get("negative_marks","")
		Question = request.data.get("question","")
		Solution = request.data.get("solution","")
		options = request.data.getlist("options","")
		if section:
			question.section = section
		if marks:
			question.marks = marks
		if nm:
			question.negative_marks=negative_marks
		if Question:
			question.question=Question
		if Solution:
			question.correct_ans=Solution
		if MultipleAnswer.objects.filter(question=question).exists():
			answers = MultipleAnswer.objects.filter(question=question)
			for i in range(len(options)):
				if answers.filter(option=options[i]).exists():
					answer = answers.get(option=options[i])
					answer.option = options[i]
					data["success"] = 'Question Saved Successfully'
				else:
					data = MultipleAnswer(
						question=question,
						option = options[i]
						).save()
					data["success"] = 'Question Saved Successfully'
					return Response(data)
		data["success"] = 'Question Saved Successfully'
		question.save()
		return Response(data)

@api_view(['POST'])
def loginStudent(request):
	data = {}
	if request.method=="POST":
		username = request.data.get('username', '')
		password1 = request.data.get('password1', '')
		rememberMe = request.data.get('remember',False)
		max_age = None
		if rememberMe:
			max_age = 60*60*24*365*10
		inst_names = SignupStudent.objects.values('firstName', 'password', 'snum','avatar','photo')
		for item in inst_names:
			print(item,username,password1)
			if item['firstName'] == username and item['password'] == password1:
				request.session['Student'] = item['snum']
				data["success"] = 'Student Logged In Successfully'
				responce = Response(data)
				responce.set_cookie('StudentName',item['firstName'], max_age = max_age)
				responce.set_cookie('StudentAvatar',item['avatar'], max_age = max_age)
				responce.set_cookie('StudentPhoto',item['photo'], max_age = max_age)
				return responce
		data["error"] = 'Invalid Credentials'
		return Response(data)

@api_view(['POST'])
def signupStudent(request):
	data = {}
	if request.method=="POST":
		firstName = request.data.get('firstName', '')
		count= SignupStudent.objects.all().count()
		count=count+1
		name= request.data.get('firstName', '')
		ch1=str("%04d" % count)
		ch2=str(name[0:2])
		studentCode=ch2+ch1
		lastName = request.data.get('lastName', '')
		email = request.data.get('email', '')
		latitude = request.data.get('cityLat')
		longitude = request.data.get('cityLng')
		username = email
		password = request.data.get('password', '')
		phone = request.data.get('phone', '')
		location = request.data.get('loc')
		if firstName.isalpha() == False | lastName.isalpha() == False :
			data["error"] = 'Name must be alphabetical'
			return Response(data)
		elif len(phone) != 10:
			data["error"] = 'Phone Number must be 10 digits'
			return Response(data)
		elif phone.isdigit() == False:
			data["error"] = 'Phone Number must be numeric'
			return Response(data)
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
			data["success"] = 'Student Created Successfully'
			return Response(data)
		data["error"] = 'error occured'
		return Response(data)

@api_view(['POST'])
def profileStudent(request):
	data = {}
	studentLoggedin = request.session.get('Student')
	if(not studentLoggedin):
		data["error"] = "Student Not logged In"
		return Response(data)
	studentObj = SignupStudent.objects.get(snum=studentLoggedin)

	if request.method == "GET":
		serializer = SignupStudentSerializer(studentObj,many=False)
		return Response(serializer.data)

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
			data["success"] = "Email Validated Successfully"
			return Response(data)
		else:
			firstName = request.data.get('firstName')
			lastName = request.data.get('lastName')
			phone = request.data.get('phone')
			oldPassword = request.data.get('oldPassword')
			newPassword = request.data.get('newPassword')
			confPassword = request.data.get('confirmPassword')
			location = request.data.get('loc')
			image = request.data.get('photo')
			latitude = request.data.get('cityLat')
			longitude = request.data.get('cityLng')
			schoolName = request.data.get('schoolName',"")
			if(not phone.isdigit()):
				data["error"] = 'Phone number should be numeric.'
				return Response(data)
			if(len(phone)!=10):
				data["error"] = "Phone number should be 10 digits long."
				return Response(data)
			if(len(newPassword)<3 or len(newPassword)>20):
				data["error"] = "Password length should be between 3 and 20"
				return Response(data)
			if(oldPassword!=studentObj.password):
				data["error"] = "Enter you correct old password."
				return Response(data)
			if(newPassword!=confPassword):
				data["error"] = "New Password and Confirm Password donot match"
				return Response(data)
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
			studentObj = SignupStudent.objects.get(snum=studentLoggedin)
			data["success"] = "data Saved Successfully"
			responce = Response(data)
			responce.set_cookie('StudentAvatar',studentObj.avatar)
			responce.set_cookie('StudentPhoto',studentObj.photo)
			return responce


@api_view(['POST'])
def searchCoachingCenter(request):
	data = {}
	if request.method == "POST":
		feeVisible = request.data.get('feeVisible')
		filDistance = request.data.get('distance')
		if filDistance=='':
			filDistance = 10**3
		la1 = float(request.data.get('cityLat',0))
		lo1 = float(request.data.get('cityLng',0))
		searchQuery = Q(showFees=True) if(feeVisible) else Q(showFees=False)
		alldata = SignupCoachingCentre.objects.filter(searchQuery)
		finaldata = []
		for x in alldata:
			la2 = x.latitude
			lo2 = x.longitude
			distance = distanceBwAB((la1,lo1),(la2,lo2)).km
			if(float(filDistance)>=float(distance)):
				finaldata.append(x)
		if finaldata:
			serializer = SignupCoachingCenterSerializer(finaldata,many=True)
			return Response(serializer.data)
		else:
			data["error"] = 'No Result Found'
			return Response(data)

@api_view(['POST'])
def enrolledTutors(request):
	data = {}
	if(request.method=='POST'):
		searchQuery = SignupTutor.objects.all()
		className = request.data.get('className',"")
		courceName = request.data.get('courseName',"")
		budgetVal = request.data.get('budget',"")
		la1 = request.data.get('cityLat',"")
		lo1 = request.data.get('cityLng',"")
		if(courceName):
			searchQuery = searchQuery.filter(signupTutorContinued__courseName=courceName)
		if(className):
			searchQuery = searchQuery.filter(signupTutorContinued__forclass=className)
		alldata = searchQuery
		finaldata = []
		if la1 and lo1:
			for x in alldata:
				la2 = float(x.latitude)
				lo2 = float(x.longitude)
				distance = distanceBwAB((float(la1),float(lo1)),(la2,lo2)).km
				if(float(x.distance)<=float(distance)):
					finaldata.append(x)
		
		if finaldata:
			serializer = SignupTutorSerializer(finaldata,many=True)
			return Response(serializer.data)
		else:
			data["error"] = 'No Result Found'
			return Response(data)

@api_view(['POST',"GET"])
def postAssignment(request):
	data = {}
	studentLoggedin = request.session.get('Student')
	if not studentLoggedin:
		data["error"] = 'Student Not Logged In'
		return Response(data)
	currentS = SignupStudent.objects.get(snum=studentLoggedin)
	if request.method == "GET":
		assignment = PostAssignment.objects.filter(connector=currentS)
		serializer = SignupStudentPostAssignmentSerializer(assignment,many=True)
		return Response(serializer.data)

	if(request.method=='POST'):
		postAssigObj = PostAssignment(
				connector = currentS,
				courseName = request.data.get('ctn'),
				forclass = request.data.get('cn'),
				description = request.data.get('description'),
				descriptionFile = request.FILES.get('file'),
				requirement = request.data.get('requirement'),
				budget = request.data.get('budget'),
			)
		postAssigObj.save()
		data["success"] = 'data Saved Successfully'
		return Response(data)

@api_view(['POST',"GET"])
def postTution(request):
	data = {}
	studentLoggedin = request.session.get('Student')
	if not studentLoggedin:
		data["error"] = 'Student Not Logged In'
		return Response(data)
	currentS = SignupStudent.objects.get(snum=studentLoggedin)
	if request.method == "GET":
		assignment = PostTution.objects.filter(connector=currentS)
		serializer = SignupStudentPostTuitionSerializer(assignment,many=True)
		return Response(serializer.data)

	if(request.method=='POST'):
		postTutionObj = PostTution(
				connector = currentS,
				courseName = request.data.get('ctn'),
				forclass = request.data.get('cn'),
				teachingMode = request.data.get('tm'),
				genderPreference = request.data.get('gp'),
				whenToStart = request.data.get('sd'),
				description = request.data.get('description'),
				budget = request.data.get('budget'),
				budgetVal = request.data.get('budgetvalue',0),
				numberOfSessions =request.data.get('monthlydigit',0)
			)
		postTutionObj.save()
		data["success"] = 'data Saved Successfully'
		return Response(data)

@api_view(['POST',])
def SearchCourses(request):
	institute = TutorialInstitute.objects.all()
	tutorials = TutorialTutors.objects.all()
	if request.method=='POST':
		srch = request.data.get('srch','')
		coursetype = request.data.get('type','')
		duration = request.data.get('duration','')
		fees = request.data.get('fees','')
		if srch:
			institute = institute.filter(Q(Title__icontains=srch))
			tutorials = tutorials.filter(Q(Title__icontains=srch))	
		if coursetype:
			institute = institute.filter(Q(Course=AddCourses.objects.get(s_num=coursetype)))
			tutorials = tutorials.filter(Q(Course=AddCourses.objects.get(s_num=coursetype)))
		if duration:
			if institute.exists():
				institute = institute.filter(Duration=duration)
			if tutorials.exists():
				tutorials = tutorials.filter(Duration=duration)
		if fees:
			fees = fees.split('-')
			if institute.exists():
				institute = institute.filter(Q(Fees__gte=fees[0]) & Q(Fees__lte=fees[1]))
			if tutorials.exists():
				tutorials = tutorials.filter(Q(Fees__gte=fees[0]) & Q(Fees__lte=fees[1]))

		ins,tut = [],[]
		if institute:
			ins = CoachingCenterTutorialInstituteSerializer(institute,many=True)
		if tutorials:
			tut = TutorAddTutorialSerializer(institute,many=True)
		if ins and tut:
			data = tut.extend(ins)
			return Response(data)
		elif ins:
			return Response(ins.data)
		else:
			return Response(tut.data)


@api_view(["GET"])
def StudentNotesAll(request):
	institue  = NotesInstitute.objects.all()
	tutor = NotesTutor.objects.all()
	institue = CoachingCenterNotesSerializer(institue,many=True)
	tutor = TutorAddNoteSerializer(tutor,many=True)

	if tutor and institue:
		data = list(chain(tutor.data,institue.data))
		return Response(data)
	elif tutor:
		return Response(tutor.data)
	else:
		return Response(institue.data)

@api_view(["GET"])
def SearchNotes(request,srch):
	institue  = NotesInstitute.objects.filter(Q(title__icontains=srch) | Q(subject__icontains=srch) | Q(description__icontains=srch))
	tutor = NotesTutor.objects.filter(Q(title__icontains=srch) | Q(subject__icontains=srch) | Q(description__icontains=srch))
	institue = CoachingCenterNotesSerializer(institue,many=True)
	tutor = TutorAddNoteSerializer(tutor,many=True)

	if tutor and institue:
		data = list(chain(tutor.data,institue.data))
		return Response(data)
	elif tutor:
		return Response(tutor.data)
	else:
		return Response(institue.data)

@api_view(["GET"])
def StudentExamsResultAll(request):
	data = {}
	studentLoggedin = request.session.get('Student')
	if not studentLoggedin:
		data["error"] = 'Student Not Logged In'
		return Response(data)
	student = SignupStudent.objects.get(snum=studentLoggedin)
	statuses = []
	if StudentMapping.objects.filter(student=student).exists():
		mapping = StudentMapping.objects.filter(student=student).first()
		results = StudentExamResult.objects.filter(student=mapping)
		serializer = StudentExamResultSerializer(results,many=True)
		return Response(serializer.data)
	else:
		data["error"] = "No result Found"
		return Response(data)


@api_view(["GET"])
def StudentExamsAll(request):
	data = {}
	studentLoggedin = request.session.get('Student')
	if not studentLoggedin:
		data["error"] = 'Student Not Logged In'
		return Response(data)
	student = SignupStudent.objects.get(snum=studentLoggedin)
	statuses = []
	if AddStudentInst.objects.filter(conector=student).exists():
		institutestudent = AddStudentInst.objects.get(conector=student)
		institute = SignupCoachingCentre.objects.filter(Q(instituteCode=institutestudent.instituteCode)&Q(instituteName=institutestudent.instituteName))
		result = []
		if institute:
			exams = Exam.objects.filter(center=institute[0])
			if exams:
				for exam in exams:
					if StudentMapping.objects.filter(student=student,exam=exam).exists():
						items = StudentMapping.objects.filter(student=student,exam=exam)
						result.extend(StudentMappingSerializer(items,many=True).data)
			return Response(result)

		else:
			data["error"] = 'Not enrolled'
			return Response(data)

@api_view(["POST","GET"])
def PostReviewTutorTutorials(request,Course_id):
	data = {}
	studentLoggedin = request.session.get('Student')
	if not studentLoggedin:
		data["error"] = 'Student Not Logged In'
		return Response(data)
	student = SignupStudent.objects.get(snum=studentLoggedin)
	try:
		tutorial = TutorialTutors.objects.get(id=Course_id)
	except:
		data["error"] = "Tutorial Doesn't Exist"
		return Response(data)

	if request.method == "GET":
		reviews = ReviewsTutor.objects.filter(Tutor=tutorial)
		serializer = TutorTutorialsReviewsSerializer(reviews,many=True)
		return Response(serializer.data)

	if request.method == "POST":
		rating =request.data.get("rating","")
		comment = request.data.get("comment","")
		print(rating,comment)
		data = ReviewsTutor(
			Tutor = tutorial,
			Student = student,
			Review=comment,
			Rating = rating,
			)
		data.save()
		data["success"] = 'Review Posted Successfully'
		return Response(data)


@api_view(["POST","GET"])
def PostReviewInstituteTutorials(request,Course_id):
	data = {}
	studentLoggedin = request.session.get('Student')
	if not studentLoggedin:
		data["error"] = 'Student Not Logged In'
		return Response(data)
	student = SignupStudent.objects.get(snum=studentLoggedin)
	try:
		tutorial = TutorialInstitute.objects.get(id=Course_id)
	except:
		data["error"] = "Tutorial Doesn't Exist"
		return Response(data)

	if request.method == "GET":
		reviews = ReviewsInstitute.objects.filter(Institute=tutorial)
		serializer = CenterTutorialsReviewsSerializer(reviews,many=True)
		return Response(serializer.data)

	if request.method == "POST":
		rating =request.data.get("rating","")
		comment = request.data.get("comment","")
		print(rating,comment)
		data = ReviewsInstitute(
			Institute = tutorial,
			Review=comment,
			Student = student,
			Rating = rating,
			)
		data.save()
		data["success"] = 'Review Posted Successfully'
		return Response(data)

@api_view(["GET"])
def InstitutesDetails(request,pk):
	data = {}
	try:
		institute = SignupCoachingCentre.objects.get(s_no=pk)
	except:
		data["error"] = "Center Doesn't Exist"
		return Response(data)
	
	reviews = InstituteRatings.objects.filter(Institute=institute).aggregate(Avg('Rating'))
	details = {"Avg_Rating":reviews["Rating__avg"]} 
	serializer = SignupCoachingCenterSerializer(institute,many=False)
	courses = AddCourses.objects.filter(coachingCentre=institute)
	details.update(serializer.data)
	for course in courses:
		details[course.courseName]= course.forclass.split(",")
	return Response(details)



@api_view(["GET"])
def TutorsDetail(request,pk):
	data = {}
	try:
		institute = SignupTutor.objects.get(sno=pk)
	except:
		data["error"] = "Tutor Doesn't Exist"
		return Response(data)
	reviews = TutorRatings.objects.filter(Tutor=institute).aggregate(Avg('Rating'))
	details = {"Avg_Rating":reviews["Rating__avg"]} 
	serializer = SignupTutorSerializer(institute,many=False)
	details.update(serializer.data)
	return Response(details)

@api_view(["POST","GET"])
def ReviewInstitute(request,inst_id):
	data = {}
	studentLoggedin = request.session.get('Student')
	if not studentLoggedin:
		data["error"] = 'Student Not Logged In'
		return Response(data)
	student = SignupStudent.objects.get(snum=studentLoggedin)
	try:
		institute = SignupCoachingCentre.objects.get(s_no=inst_id)
	except:
		data["error"] = "Center Doesn't Exist"
		return Response(data)

	if request.method == "GET":
		reviews = InstituteRatings.objects.filter(Institute=institute)
		serializer = CenterReviewsSerializer(reviews,many=True)
		return Response(serializer.data)

	if request.method == "POST":
		rating =request.data.get("rating","")
		comment = request.data.get("comment","")
		print(rating,comment)
		data = InstituteRatings(
			Institute = institute,
			Review=comment,
			Student = student,
			Rating = rating,
			)
		data.save()
		data["success"] = 'Review Posted Successfully'
		return Response(data)

@api_view(["POST","GET"])
def ReviewTutors(request,tutor_id):
	data = {}
	studentLoggedin = request.session.get('Student')
	if not studentLoggedin:
		data["error"] = 'Student Not Logged In'
		return Response(data)
	student = SignupStudent.objects.get(snum=studentLoggedin)
	try:
		institute = SignupTutor.objects.get(sno=tutor_id)
	except:
		data["error"] = "Tutor Doesn't Exist"
		return Response(data)

	if request.method == "GET":
		reviews = TutorRatings.objects.filter(Tutor=institute)
		serializer = TutorReviewsSerializer(reviews,many=True)
		return Response(serializer.data)

	if request.method == "POST":
		rating =request.data.get("rating","")
		comment = request.data.get("comment","")
		print(rating,comment)
		data = TutorRatings(
			Tutor = institute,
			Review=comment,
			Student = student,
			Rating = rating,
			)
		data.save()
		data["success"] = 'Review Posted Successfully'
		return Response(data)
