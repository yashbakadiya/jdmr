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
from buy_items.models import BuyInstituteNotes,BuyTutorNotes
from students.models import AddStudentInst
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
            price = request.POST.get("price","")
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
                        price = price,
                        description = description,
                        )
                    try:
                        data.save()
                        return redirect('addnotes')
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
            price = request.POST.get("price","")
            description = request.POST.get("description","")
            course = request.POST.get("course","")
            course = Courses.objects.get(id=course).courseName
            forclass = request.POST.get('forclass','')

            if note:
                data.notes = note[0]
            if title:
                data.title = title
            if price:
                data.price = price
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
                        price = price,
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
            price = request.POST.get("price","")
            forclass = request.POST.get("forclass","")
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
                        price = price,
                        forclass = forclass,
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
            price = request.POST.get("price","")

            if note:
                data.notes = note[0]
            if title:
                data.title = title
            if price:
                data.price = price
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
                        price = price,
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
            #institute
            #buy institute notes list
            buy_institute_notes = BuyInstituteNotes.objects.filter(student=student)
            buy_institute_notes_list = [buy.note.id for buy in buy_institute_notes]
            bought_institute_notes = NotesInstitute.objects.filter(id__in=buy_institute_notes_list).order_by("-id")
            #not bought institute notes list
            not_bought_institute_notes = NotesInstitute.objects.all().exclude(id__in=buy_institute_notes_list).order_by("-id")

            #tutor
            #buy tutor notes list
            buy_tutor_notes = BuyTutorNotes.objects.filter(student=student)
            buy_tutor_note_list = [buy.note.id for buy in buy_tutor_notes]
            bought_tutor_notes = NotesTutor.objects.filter(id__in=buy_tutor_note_list).order_by("-id")
            #not bought tutor notes list
            not_bought_tutor_notes = NotesTutor.objects.all().exclude(id__in=buy_tutor_note_list).order_by("-id")
            print(bought_tutor_notes, not_bought_tutor_notes)
            context['bought_institute_notes'] = bought_institute_notes
            context['not_bought_institute_notes'] = not_bought_institute_notes
            context['bought_tutor_notes'] = bought_tutor_notes
            context['not_bought_tutor_notes'] = not_bought_tutor_notes

        return render(request,'Notes/allnotes.html',context=context)
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

def viewInstituteNotesPDF(request,pk):
    return render(request,'Notes/notesview.html',{'note':NotesInstitute.objects.get(id=pk)})

def viewTutorNotesPDF(request,pk):
    return render(request,'Notes/notesview.html',{'note':NotesTutor.objects.get(id=pk)})