from django.shortcuts import render,HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from accounts.models import Student
from notes.models import NotesInstitute, NotesTutor
from tutorials.models import TutorialInstitute
from .models import BuyInstituteNotes,BuyTutorNotes, BuyTutorial


# buy institute notes
login_required(login_url='login')
def buyInstituteNotes(request,id):
    errors = []
    if request.session['type'] == "student":
        if request.method == "GET":
            user = User.objects.get(username=request.session['user'])
            student = Student.objects.get(user=user)
            note = NotesInstitute.objects.get(id=id)
            if int(note.price) == 0:
                data = BuyInstituteNotes.objects.create(
                    student=student,
                    status=1,
                    note=note
                )
                try:
                    data.save()
                    return redirect('notesstudents')
                except:
                    errors.append("Some error Occured! Try Again")
                    context['errors'] = errors
                    return redirect('notesstudents')
        
        # else:
        #     user = User.objects.get(username=request.session['user'])
        #     student = Student.objects.get(user=user)
        #     if request.method == "POST":
        #         status = request.POST.get("status")
        #         note = NotesInstitute.objects.get(id=id)
        #         if (note and status):
        #             data = BuyInstituteNotes.objects.create(
        #                 note = note,
        #                 status = status,
        #                 student = student
        #             )
        #             try:
        #                 data.save()
        #                 return redirect('')
        #             except:
        #                 errors.append("Some error Occured! Try Again")
        #                 context['errors'] = errors
        #     return render(request,'',context)
    return HttpResponse("You are Not Authenticated for this page")


# buy tutor notes
login_required(login_url='login')
def buyTutorNotes(request,id):
    errors = []
    if request.session['type'] == "student":
        if request.method == "GET":
            return render(request, '')
        else:
            user = User.objects.get(username=request.session['user'])
            student = Student.objects.get(user=user)
            if request.method == "POST":
                status = request.POST.get("status")
                note = NotesTutor.objects.get(id=id)
                if (note and status):
                    data = BuyTutorNotes.objects.create(
                        note = note,
                        status = status,
                        student = student
                    )
                    try:
                        data.save()
                        return redirect('')
                    except:
                        errors.append("Some error Occured! Try Again")
                        context['errors'] = errors
            return render(request,'',context)
    return HttpResponse("You are Not Authenticated for this page")


# buy tutorial
login_required(login_url='login')
def buyTutorial(request, id):
    errors = []
    if request.session['type'] == "student":
        if request.method == "GET":
            return render(request, '')
        else:
            user = User.objects.get(username=request.session['user'])
            student = Student.objects.get(user=user)
            if request.method == "POST":
                status = request.POST.get("status")
                tutorial = TutorialInstitute.objects.get(id=id)
                if (tutorial and status):
                    data = BuyNotes.objects.create(
                        note = note,
                        status = status,
                        student = student
                    )
                    try:
                        data.save()
                        return redirect('')
                    except:
                        errors.append("Some error Occured! Try Again")
                        context['errors'] = errors
            return render(request,'',context)
    return HttpResponse("You are Not Authenticated for this page")


# list student buyed notes
login_required(login_url='login')
def StudentBuyNotesList(request):
    if request.session['type'] == "Student":
        user = User.objects.get(username=request.session['user'])
        student = Student.objects.get(user=user)
        notes = BuyNotes.objects.filter(student=student).filter(status=1)
        context = {
            "notes":notes,
        }
        return render(request, "", context=context)
    else:
        return HttpResponse("you can not access this page")


# list student buyed tutorials
login_required(login_url='login')
def StudentBuyTutorialList(request):
    if request.session['type'] == "Student":
        user = User.objects.get(username=request.session['user'])
        student = Student.objects.get(user=user)
        tutorials = BuyTutorial.objects.filter(student=student).filter(status=1)
        context = {
            "tutorials" = tutorials,
        }
        return render(request, "", context=context)
    else:
        return HttpResponse("you can not access this page")
