from django.shortcuts import render,HttpResponse,redirect,HttpResponseRedirect
from accounts.models import Institute,Student,Teacher
from django.contrib.auth.decorators import login_required
from courses.models import Courses,TeachingType
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.models import User
from .models import *
from datetime import datetime,timedelta
# Create your views here.

@login_required(login_url="Login")
def addTutorialsInstitute(request):
    if request.session["type"] == "Institute":
        user = User.objects.get(username=request.session['user'])
        inst = Institute.objects.get(user=user)
        courses = Courses.objects.filter(intitute=inst,archieved=False)
        context = {
        'courses':courses
        }
        if request.method == "POST":
            print(request.POST)
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
                Course = Courses.objects.get(intitute=inst,courseName=course),
                Fees = fees,
                Duration = duration,
                Description = description,
                Validity = discValidity,
                Discount = feeDisc,
                )
            data.save()
            return redirect('addplaylist',data.id)
        return render(request,'tutorials/addTutorialsInstitute.html',context)
    return HttpResponse("You Are not Authenticated User for this Page")


@login_required(login_url="Login")
def ViewTutorials(request):
    if request.session['type'] == 'Institute':
        user = User.objects.get(username=request.session['user'])
        inst = Institute.objects.get(user=user)
        courses = Courses.objects.filter(intitute=inst,archieved=False)
        tutorials = []
        try:
            for i in courses:
                if TutorialInstitute.objects.filter(Course=i).exists():
                    print(TutorialInstitute.objects.filter(Q(Course=i) & Q(Archived=False)))
                    tutorials.extend(TutorialInstitute.objects.filter(Q(Course=i) & Q(Archived=False)))
        except:
            tutorials=[]

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
        return render(request,'tutorials/viewTutorials.html',context)
    return HttpResponse("You Are not Authenticated User for this Page")


@login_required(login_url="Login")
def ArchiveTutorials(request):
    if request.session['type'] == "Institute":
        user = User.objects.get(username=request.session['user'])
        inst = Institute.objects.get(user=user)
        courses = Courses.objects.filter(intitute= inst)
        tutorials = []
        for i in courses:
            if TutorialInstitute.objects.filter(Course=i).exists():
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
        return render(request,'tutorials/ArchievedTutorials.html',context)
    return HttpResponse("You Are not Authenticated User for this Page")


@login_required(login_url="Login")
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
			return render(request,'tutorials/AddTutorCourseVideos.html',{'errors':errors})
		return redirect('viewtutorials')
	return render(request,'tutorials/AddTutorCourseVideos.html')


@login_required(login_url="Login")
def DeleteTutorialsInstitute(request,course_id):
    if request.session['type'] == "Institute":
        data = TutorialInstitute.objects.get(id=course_id)
        data.delete()
        messages.warning(request,"Tutorial Deleted Successfully")
        return redirect('viewtutorials')
    return HttpResponse("You Are not Authenticated User for this Page")



@login_required(login_url="Login")
def EditTutorialsInstitute(request,course_id):
    if request.session['type'] == "Institute":
        user = User.objects.get(username=request.session['user'])
        inst = Institute.objects.get(user=user)
        courses = Courses.objects.filter(intitute=inst)
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
            messages.success(request,"Tutorial Updated Successfully")
            return redirect('viewtutorials')
        return render(request,'tutorials/editTutorial.html',context)
    return HttpResponse("You Are not Authenticated User for this Page")


@login_required(login_url="Login")
def WatchTutorialsInstitute(request,course_id):
    if request.session['type']=="Institute":
        user = User.objects.get(username=request.session['user'])
        inst = Institute.objects.get(user=user)
        courses = Courses.objects.filter(intitute=inst,archieved=False)
        tutorial = TutorialInstitute.objects.get(id=course_id)
        print('tutorial--',tutorial)
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
        return render(request,'tutorials/watchTutorial.html',context)
    return HttpResponse("You Are not Authenticated User for this Page")


@login_required(login_url="Login")
def DeleteTutorialsInstituteVideos(request,playlist_id):
    if request.session['type']=="Institute":
        data = TutorialInstitutePlaylist.objects.get(id=playlist_id)
        data.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required(login_url="Login")
def EditTutorialsInstituteVideos(request,playlist_id):
    if request.session['type']=="Institute":
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
        return render(request,'tutorials/editTutorialVideos.html',context)


@login_required(login_url="Login")
def addTutorialsTutor(request):
    if request.session['type']=="Teacher":
        user = User.objects.get(username=request.session['user'])
        tutor = Teacher.objects.get(user=user)
        context = {}
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
        return render(request,'tutorials/addTutorialsTutor.html',context)
    return HttpResponse("You Are not Authenticated User for this Page")


@login_required(login_url="Login")
def addTutorialsTutorVideos(request,course_id):
    if request.session["type"]=="Teacher":
        user = User.objects.get(username=request.session['user'])
        tutor = Teacher.objects.get(user=user)
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
                return render(request,'tutorials/AddTutorCourseVideos.html',{'errors':errors})
            return redirect('viewtutorialstutor')
        return render(request,'tutorials/AddTutorCourseVideos.html')
    return HttpResponse("You Are not Authenticated User for this Page")



@login_required(login_url="Login")
def ViewTutorialsTutor(request):
    if request.session['type']=="Teacher":
        user = User.objects.get(username=request.session['user'])
        tutor = Teacher.objects.get(user=user)
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
        return render(request,'tutorials/viewTutorialsTutor.html',context)
    return HttpResponse("You Are not Authenticated User for this Page")



@login_required(login_url="Login")
def WatchTutorialsTutor(request,course_id):
    if request.session['type']=="Teacher":
        user = User.objects.get(username=request.session['user'])
        tutor = Teacher.objects.get(user=user)
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
        return render(request,'tutorials/watchTutorialTutor.html',context)
    return HttpResponse("You Are not Authenticated User for this Page")



@login_required(login_url="Login")
def DeleteTutorialsTutor(request,course_id):
    if request.session['type']=="Teacher":
        data = TutorialTutors.objects.get(id=course_id)
        data.delete()
        return redirect('viewtutorialstutor')
    return HttpResponse("You Are not Authenticated User for this Page")


@login_required(login_url="Login")
def DeleteTutorialsTutorVideos(request,playlist_id):
    if request.session['type']=="Teacher":
        data = TutorialTutorsPlaylist.objects.get(id=playlist_id)
        data.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    return HttpResponse("You Are not Authenticated User for this Page")


@login_required(login_url="Login")
def EditTutorialsTutorVideos(request,playlist_id):
    if request.session['type']=="Teacher":
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
        return render(request,'tutorials/editTutorialVideosTutor.html',context)
    return HttpResponse("You Are not Authenticated User for this Page")



@login_required(login_url="Login")
def EditTutorialsTutor(request,course_id):
    if request.session['type']=="Teacher":
        user = User.objects.get(username=request.session['user'])
        tutor = Teacher.objects.get(user=user)
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
        return render(request,'tutorials/editTutorialTutor.html',context)
    return HttpResponse("You Are not Authenticated User for this Page")



@login_required(login_url="Login")
def ArchiveTutorialsTutor(request):
    if request.session['type']=="Teacher":
        user = User.objects.get(username=request.session['user'])
        tutor = Teacher.objects.get(user=user)
        tutorials = TutorialTutors.objects.filter(Q(Tutor=tutor) & Q(Archived=True))
        context = {
        'tutorials':tutorials
        }
        if request.method == "POST":
            ids = request.POST.getlist('ids')
            if len(ids)<1:
                return redirect('Archivetutorialstutor')
            for i in ids:
                if TutorialTutors.objects.filter(id=i).exists():
                    tutorial = TutorialTutors.objects.get(id=int(i))
                    tutorial.Archived = False
                    tutorial.save()
            return redirect('Archivetutorialstutor')
        return render(request,'tutorials/ArchievedTutorialsTutor.html',context)
    return HttpResponse("You Are not Authenticated User for this Page")


@login_required(login_url="Login")
def SearchCourses(request):
	tutorials = TutorialTutors.objects.all()
	extra  = TutorialInstitute.objects.all()
	courses = Courses.objects.all()
	if request.method=='POST':
		coursetype = request.POST.get('type','')
		duration = request.POST.get('duration','')
		fees = request.POST.get('fees','')
		if coursetype:
			extra = TutorialInstitute.objects.all().filter(Q(Course=AddCourses.objects.get(s_num=coursetype)))
			course = Courses.objects.get(s_num=coursetype).courseName
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
		'alltutorials':tutorials,
		'courses':courses
		}
		return render(request,'tutorials/SearchCourses.html',context)
	alltutorials = tutorials.union(extra).order_by('Title')
	context = {
    'alltutorials':alltutorials,
	'courses':courses
	}
	return render(request,'tutorials/SearchCourses.html',context)


@login_required(login_url="Login")
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
	return render(request,'tutorials/watchTutorialStudent.html',context)


@login_required(login_url="Login")
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
	return render(request,'tutorials/watchTutorialStudent.html',context)
