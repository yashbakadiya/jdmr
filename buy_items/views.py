from django.shortcuts import render,HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from accounts.models import Student
from notes.models import NotesInstitute, NotesTutor
from tutorials.models import TutorialInstitute, TutorialTutors
from .models import BuyInstituteNotes,BuyTutorNotes, BuyTutorTutorial, BuyInstituteTutorial

login_required(login_url='login')
def check(request):
    return HttpResponse("You Are Not Authenticated for this Page")

# buy institute notes
login_required(login_url='login')
def buyInstituteNotes(request,id):
    errors = []
    if request.session['type'] == "Student":
        user = User.objects.get(username=request.session['user'])
        student = Student.objects.get(user=user)
        note = NotesInstitute.objects.get(id=id)
        if request.method == "GET":
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
            else:
                return render(request, 'buy/buy_institute_note.html', context={'note':note})
        elif request.method == "POST":
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
        return HttpResponse("Unknown error")
    return HttpResponse("You are Not Authenticated for this page")

# buy tutor notes
login_required(login_url='login')
def buyTutorNotes(request,id):
    errors = []
    if request.session['type'] == "Student":
        user = User.objects.get(username=request.session['user'])
        student = Student.objects.get(user=user)
        note = NotesTutor.objects.get(id=id)
        if request.method == "GET":
            if int(note.price) == 0:
                data = BuyTutorNotes.objects.create(
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
            else:
                return render(request, 'buy/buy_tutor_note.html', context={'note':note})
        elif request.method == "POST":
            data = BuyTutorNotes.objects.create(
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
        return HttpResponse("Unknown error")
    return HttpResponse("You are Not Authenticated for this page")


login_required(login_url='login')
def buyTutorTutorial(request, id):
    errors = []
    if request.session['type'] == 'Student':
        user = User.objects.get(username=request.session['user'])
        student = Student.objects.get(user=user)
        tutorial = TutorialTutors.objects.get(id=id)
        if request.method == "GET":
            if int(tutorial.Fees) == 0:
                data = BuyTutorTutorial.objects.create(
                    student=student,
                    status=1,
                    tutorial=tutorial
                )
                try:
                    data.save()
                    return redirect('searchcourses')
                except:
                    errors.append("Some error Occured! Try Again")
                    context['errors'] = errors
                    return redirect('searchcourses')
            else:
                return render(request, 'buy/buy_tutor_tutorial.html', context={'tutorial':tutorial})
        elif request.method == "POST":
            data = BuyTutorTutorial.objects.create(
                    student=student,
                    status=1,
                    tutorial=tutorial
                )
            try:
                data.save()
                return redirect('searchcourses')
            except:
                errors.append("Some error Occured! Try Again")
                context['errors'] = errors
                return redirect('searchcourses')
        return HttpResponse("Unknown error")
    return HttpResponse("You are Not Authenticated for this page")



login_required(login_url='login')
def buyInstituteTutorial(request, id):
    errors = []
    if request.session['type'] == 'Student':
        user = User.objects.get(username=request.session['user'])
        student = Student.objects.get(user=user)
        tutorial = TutorialInstitute.objects.get(id=id)
        if request.method == "GET":
            if int(tutorial.Fees) == 0:
                data = BuyInstituteTutorial.objects.create(
                    student=student,
                    status=1,
                    tutorial=tutorial
                )
                try:
                    data.save()
                    return redirect('searchcourses')
                except:
                    errors.append("Some error Occured! Try Again")
                    context['errors'] = errors
                    return redirect('searchcourses')
            else:
                return render(request, 'buy/buy_Institute_tutorial.html', context={'tutorial':tutorial})
        elif request.method == "POST":
            data = BuyInstituteTutorial.objects.create(
                    student=student,
                    status=1,
                    tutorial=tutorial
                )
            try:
                data.save()
                return redirect('searchcourses')
            except:
                errors.append("Some error Occured! Try Again")
                context['errors'] = errors
                return redirect('searchcourses')
        return HttpResponse("Unknown error")
    return HttpResponse("You are Not Authenticated for this page")

