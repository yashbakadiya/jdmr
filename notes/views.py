from django.shortcuts import render,HttpResponse,HttpResponseRedirect,redirect
from accounts.models import Institute, Student,Teacher
from courses.models import Courses
from .models import NotesInstitute,NotesTutor
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from teacher.models import enrollTutors
from batches.models import BatchTiming
from students.models import *
from itertools import chain
# Create your views here.


@login_required(login_url="Login")
def AddNotesInstitute(request):
    errors = []
    if request.session['type'] == "Institute":
        user = User.objects.get(username=request.session['user'])
        inst = Institute.objects.get(user=user)
        classes = Courses.objects.filter(intitute=inst).values_list('forclass')
        notes = NotesInstitute.objects.filter(institute=inst)
        context = {
        'notes':notes,
        'classes':classes
        }
        if request.method == "POST":
            note = request.FILES.getlist("note","")
            title = request.POST.get("title","")
            description = request.POST.get("description","")
            course = request.POST.get("course","")
            course = Courses.objects.get(id=course).courseName
            forclass = request.POST.get('forclass','')
            if (note and title and description and course):
                for i in range(len(note)):
                    data = NotesInstitute(
                        institute = inst,
                        notes = note[i],
                        title = title,
                        subject = course,
                        forclass = forclass,
                        description = description,
                        )
                    try:
                        data.save()
                        return redirect('viewnotes')
                    except:
                        errors.append("Some error Occured! Try Again")
                        context['errors'] = errors
        return render(request,'Notes/addNotesInstitute.html',context)
    return HttpResponse("You are Not Authenticated for this page")
    

@login_required(login_url="Login")
def ViewNotesInstitute(request):
    if request.session["type"] == "Institute":
        user = User.objects.get(username=request.session['user'])
        inst = Institute.objects.get(user=user)    
        notes = NotesInstitute.objects.filter(institute=inst)
        context = {
        'notes':notes,
        'template':'dashboard/base.html'
        }
        
        return render(request,'Notes/allnotes.html',context)
    return HttpResponse("You are Not Authenticated for this page")
    


@login_required(login_url="Login")
def PdfViewNoteInstitute(request,note_id):
    if request.session['type']=="Institute":
        note = NotesInstitute.objects.get(id=note_id)
        context = {
        'note':note
        }
        print('path--',note.notes.url)
        return render(request,'Notes/PdfViewNotesInstitute.html',context)
    return HttpResponse("You are Not Authenticated for this page")
    


@login_required(login_url="Login")
def DeleteNoteInstitute(request,note_id):
    if request.session['type']=="Institute":
        note = NotesInstitute.objects.get(id=note_id)
        note.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



@login_required(login_url="Login")
def EditNoteInstitute(request,note_id):
    if request.session['type']=="Institute":
        data = NotesInstitute.objects.get(id=note_id)
        errors = []
        user = User.objects.get(username=request.session['user'])
        inst = Institute.objects.get(user=user)
        courses = Courses.objects.filter(intitute=inst)
        context = {
        'courses':courses,
        'note':data
        }
        if request.method == "POST":
            note = request.FILES.getlist("note","")
            title = request.POST.get("title","")
            description = request.POST.get("description","")
            course = request.POST.get("course","")
            course = Courses.objects.get(id=course).courseName
            forclass = request.POST.get('forclass','')

            if note:
                data.notes = note[0]
            if title:
                data.title = title
            if description:
                data.description = description
            if course:
                data.subject = course
            if forclass:
                data.forclass = forclass
            try:
                data.save()
                return redirect('viewnotes')
            except:
                errors.append('Error Occured! Try Again')
                context['errors'] = errors

            if len(note)>1:
                for i in range(1,len(note)):
                    data = NotesInstitute(
                        institute = inst,
                        notes = note[i],
                        title = title,
                        subject = course,
                        forclass = forclass,
                        description = description,
                        )
                    try:
                        data.save()
                        return redirect('viewnotes')
                    except:
                        errors.append("Some error Occured! Try Again")
                        context['errors'] = errors
        return render(request,'Notes/editNoteInstitute.html',context)
    return HttpResponse("You are not Authenticated for this Page")


@login_required(login_url="Login")
def AddNotesTutor(request):
    if request.session['type']=="Teacher":
        errors = []
        user = User.objects.get(username=request.session['user'])
        tutor = Teacher.objects.get(user=user)
        courses = []
        if enrollTutors.objects.filter(teacher=tutor).exists():
            INSTtutor = enrollTutors.objects.get(teacher=tutor)
            INSTcourse = INSTtutor.courseName.replace(";",'')
            Tutorcourse = tutor.course.replace(";",'')
            coursesID = INSTcourse+Tutorcourse
            coursesID = list(set(coursesID))
            for i in coursesID:
                try:
                    course = Courses.objects.get(id=int(i))
                    courses.append(course)
                except:
                    pass
        else:
            Tutorcourse = tutor.course.replace(";",'')
            coursesID = list(set(Tutorcourse))
            for i in coursesID:
                try:
                    course = Courses.objects.get(id=int(i))
                    courses.append(course)
                except:
                    pass
        notes = NotesTutor.objects.filter(tutor=tutor)
        context = {
        'courses':courses,
        'notes':notes
        }
        if request.method == "POST":
            note = request.FILES.getlist("note","")
            title = request.POST.get("title","")
            description = request.POST.get("description","")
            course = request.POST.get("course","")
            print(note,title,description,course)
            if note:
                for i in range(len(note)):
                    data = NotesTutor(
                        tutor = tutor,
                        notes = note[i],
                        title = title,
                        subject = course,
                        description = description,
                        )
                    try:
                        data.save()
                        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                    except:
                        errors.append("Some error Occured! Try Again")
                        context['errors'] = errors
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        return render(request,'Notes/addNotesTutor.html',context)
    return HttpResponse("You are not Authenticated for this Page")
    


@login_required(login_url="Login")
def ViewNotesTutor(request):
    if request.session['type']=="Teacher":
        user = User.objects.get(username=request.session['user'])
        tutor = Teacher.objects.get(user=user)
        notes = NotesTutor.objects.filter(tutor=tutor)
        context = {
        'notes':notes,
        'template':'dashboard/Tutor-dashboard.html'
        }
        return render(request,'Notes/allnotes.html',context)
    return HttpResponse("You are not Authenticated for this Page")


@login_required(login_url="Login")
def EditNoteTutor(request,note_id):
    if request.session['type']=="Teacher":
        try:
            data = NotesTutor.objects.get(id=note_id)
        except:
            return HttpResponse("You are not Authenticated for this Page")
        errors = []
        user = User.objects.get(username=request.session['user'])
        tutor = Teacher.objects.get(user=user)
        courses = []
        if enrollTutors.objects.filter(teacher=tutor).exists():
            INSTtutor = enrollTutors.objects.get(teacher=tutor)
            INSTcourse = INSTtutor.courseName.replace(";",'')
            Tutorcourse = tutor.course.replace(";",'')
            coursesID = INSTcourse+Tutorcourse
            coursesID = list(set(coursesID))
            for i in coursesID:
                try:
                    course = Courses.objects.get(id=int(i))
                    courses.append(course)
                except:
                    pass
        else:
            Tutorcourse = tutor.course.replace(";",'')
            coursesID = list(set(Tutorcourse))
            for i in coursesID:
                try:
                    course = Courses.objects.get(id=int(i))
                    courses.append(course)
                except:
                    pass
        context = {
        'courses':courses,
        'note':data
        }
        if request.method == "POST":
            note = request.FILES.getlist("note","")
            title = request.POST.get("title","")
            description = request.POST.get("description","")
            course = request.POST.get("course","")

            if note:
                data.notes = note[0]
            if title:
                data.title = title
            if description:
                data.description = description
            if course:
                data.subject = course
            try:
                data.save()
                return redirect('addnotestutor')
            except:
                errors.append('Error Occured! Try Again')
                context['errors'] = errors

            if len(note)>1:
                for i in range(1,len(note)):
                    data = NotesTutor(
                        tutor = tutor,
                        notes = note[i],
                        title = title,
                        subject = course,
                        description = description,
                        )
                    try:
                        data.save()
                        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                    except:
                        errors.append("Some error Occured! Try Again")
                        context['errors'] = errors
        return render(request,'Notes/editNotesTutor.html',context)
    return HttpResponse("You are not Authenticated for this Page")


@login_required(login_url="Login")
def DeleteNoteTutor(request,note_id):
    if request.session['type']=="Teacher":
        try:
            note = NotesTutor.objects.get(id=note_id)
        except:
            return HttpResponse("Unable to Process")
        user = User.objects.get(username=request.session['user'])
        tutor = Teacher.objects.get(user=user)
        if tutor == note.tutor:
            note.delete()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            return HttpResponse("You are not Authenticated for this Page")
    return HttpResponse("You are not Authenticated for this Page")
            


def Combine_two_models(one,two):
	return chain(one,two)


@login_required(login_url="Login")
def AllNotesStudent(request):
    if request.session['type']=="Student":
        user = User.objects.get(username=request.session['user'])
        student = Student.objects.get(user=user)
        context = {}
        if AddStudentInst.objects.filter(student=student).exists():
            INSTstudent = AddStudentInst.objects.get(student=student)
            institute = NotesInstitute.objects.filter(institute=INSTstudent.institute)
            tutor = NotesTutor.objects.all()
            if tutor:
                all = Combine_two_models(institute,tutor)
            else:
                all  = institute
            print(all)
            context['notes'] = all
            context['template'] = 'dashboard/student-dashboard.html'
        return render(request,'Notes/allnotes.html',context)
    return HttpResponse('You are not Authenticated for this page')



@login_required(login_url="Login")
def ViewpdfStudentInstitute(request,note_id):
	try:
		note = NotesInstitute.objects.get(id=note_id)
	except:
		note = []
	context = {
	'note':note
	}
	return render(request,'Notes/viewpdfstudent.html',context)



@login_required(login_url="Login")
def ViewpdfTutor(request,note_id):
	try:
		note = NotesTutor.objects.get(id=note_id)
	except:
		note = []
	context = {
	'note':note
	}
	return render(request,'Notes/viewpdfstudent.html',context)


@login_required(login_url="Login")
def subjects(request):
	data = {}
	if request.is_ajax:
		classname = request.GET.get("class","")
		jsonLocalData = loads(open('cc.txt','r').read())
		if classname:
			courses = jsonLocalData[classname]
			data["categories"] = courses
	return JsonResponse(data,safe=False)