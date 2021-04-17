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
from django.contrib import messages
from buy_items.models import BuyInstituteNotes,BuyTutorNotes
from students.models import AddStudentInst
from datetime import datetime
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
            price = request.POST.getlist("price","")
            title = request.POST.getlist("title","")
            description = request.POST.getlist("description","")
            course = request.POST.get("course","")
            forclass = request.POST.get('forclass','')
            freeEnrolled = request.POST.get('enr',"0")

            if freeEnrolled == "1":
                freeEnrolled = True
            else:
                freeEnrolled = False
            if (note and title and description and course):
                for i in range(len(note)):
                    data = NotesInstitute(
                        institute = inst,
                        notes = note[i],
                        title = title[i],
                        subject = course,
                        forclass = forclass,
                        price = price[i],
                        description = description[i],
                        freeEnrolled=freeEnrolled
                        )
                    try:
                        data.save()
                    except:
                        errors.append("Some error Occured! Try Again")
                        context['errors'] = errors
                        return redirect('addnotes')
                messages.success(request,"Notes Added Successfully")
                return redirect('addnotes')
        return render(request,'Notes/addNotesInstitute.html',context)
    return HttpResponse("You are Not Authenticated for this page")
    
@login_required(login_url="Login")
def DeleteNoteInstitute(request,note_id):
    if request.session['type']=="Institute":
        note = NotesInstitute.objects.get(id=note_id)
        note.delete()
        messages.warning(request,"Notes Deleted Successfully")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url="Login")
def EditNoteInstitute(request,note_id):
    if request.session['type']=="Institute":
        data = NotesInstitute.objects.get(id=note_id)
        errors = []
        user = User.objects.get(username=request.session['user'])
        inst = Institute.objects.get(user=user)
        classes = Courses.objects.filter(intitute=inst).values_list('forclass')
        context = {
        'classes':classes,
        'note':data
        }
        if request.method == "POST":
            note = request.FILES.get("note","")
            title = request.POST.get("title","")
            price = request.POST.get("price","")
            description = request.POST.get("description","")
            course = request.POST.get("course","")
            forclass = request.POST.get('forclass','')
            freeEnrolled = request.POST.get('enr',"0")

            if freeEnrolled == "1":
                freeEnrolled = True
            else:
                freeEnrolled = False

            if note:
                data.notes = note
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
            if freeEnrolled:
                data.freeEnrolled = freeEnrolled
            data.date = datetime.now()
            try:
                data.save()
                messages.success(request,"Notes Updated Successfully")
                return redirect('addnotes')
            except:
                errors.append('Error Occured! Try Again')
                context['errors'] = errors
        return render(request,'Notes/editNoteInstitute.html',context)
    return HttpResponse("You are not Authenticated for this Page")


@login_required(login_url="Login")
def AddNotesTutor(request):
    if request.session['type']=="Teacher":
        errors = []
        user = User.objects.get(username=request.session['user'])
        tutor = Teacher.objects.get(user=user)
        notes = NotesTutor.objects.filter(tutor=tutor)

        class_list = tutor.forclass.split(',')
        unique_class = list(set(class_list))
        course_list = tutor.course.split(',')
        data = {}

        for i in  range(len(unique_class)):
            courses_of_class =[]
            for j in range(len(class_list)):
                if class_list[j] == unique_class[i]:
                    courses_of_class.append(course_list[j])
            data[unique_class[i]] = list(set(courses_of_class))

        other = False
        nursery = False

        if 'Other' in unique_class:
            unique_class.remove('Other')
            other = True
        if 'Nursery' in unique_class:
            unique_class.remove('Nursery')
            nursery = True
        
        classes = sorted(unique_class,key=lambda a:int(a))

        if other:
            classes.append('Other')
        if nursery:
            classes.insert(0,'Nursery')

        context = {
        'classes':classes,
        'data':data, 
        'notes':notes
        }
        if request.method == "POST":
            note = request.FILES.getlist("note","")
            price = request.POST.getlist("price","")
            title = request.POST.getlist("title","")
            description = request.POST.getlist("description","")
            forclass = request.POST.get("forclass","")
            course = request.POST.get("course","")
            if note:
                for i in range(len(note)):
                    data = NotesTutor(
                        tutor = tutor,
                        forclass = forclass,
                        subject = course,
                        notes = note[i],
                        title = title[i],
                        price = price[i],
                        description = description[i],
                        )
                    try:
                        data.save()
                    except:
                        errors.append("Some error Occured! Try Again")
                        context['errors'] = errors
                        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                messages.success(request,"Notes Added Successfully")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        return render(request,'Notes/addNotesTutor.html',context)
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


        class_list = tutor.forclass.split(',')
        unique_class = list(set(class_list))
        course_list = tutor.course.split(',')
        datalist = {}

        for i in  range(len(unique_class)):
            courses_of_class =[]
            for j in range(len(class_list)):
                if class_list[j] == unique_class[i]:
                    courses_of_class.append(course_list[j])
            datalist[unique_class[i]] = list(set(courses_of_class))

        other = False
        nursery = False

        if 'Other' in unique_class:
            unique_class.remove('Other')
            other = True
        if 'Nursery' in unique_class:
            unique_class.remove('Nursery')
            nursery = True
        
        classes = sorted(unique_class,key=lambda a:int(a))

        if other:
            classes.append('Other')
        if nursery:
            classes.insert(0,'Nursery')

        context = {
        'classes':classes,
        'data':datalist, 
        'note':data
        }

        if request.method == "POST":
            note = request.FILES.get("note","")
            title = request.POST.get("title","")
            price = request.POST.get("price","")
            description = request.POST.get("description","")
            course = request.POST.get("course","")
            forclass = request.POST.get('forclass','')

            if note:
                data.notes = note
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
            data.date = datetime.now()
            try:
                data.save()
                messages.success(request,"Notes Updated Successfully")
                return redirect('addnotestutor')
            except:
                errors.append('Error Occured! Try Again')
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
            messages.warning(request,"Notes Deleted Successfully")
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
            context['bought_institute_notes'] = bought_institute_notes
            context['not_bought_institute_notes'] = not_bought_institute_notes
            context['bought_tutor_notes'] = bought_tutor_notes
            context['not_bought_tutor_notes'] = not_bought_tutor_notes

        return render(request,'Notes/allnotes.html',context=context)
    return HttpResponse('You are not Authenticated for this page')

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