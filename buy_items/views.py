from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from accounts.models import Student
from notes.models import NotesInstitute, NotesTutor
from tutorials.models import TutorialInstitute, TutorialTutors
from .models import BuyInstituteNotes, BuyTutorNotes, BuyTutorTutorial, BuyInstituteTutorial, BuyTutorExam, Revenue
from exams.models import TutorExam
from django.db.models import Sum
from datetime import datetime
from dateutil.relativedelta import *
import json
import re
import requests
from django.http import JsonResponse

login_required(login_url='login')
def check(request):
    return HttpResponse("You Are Not Authenticated for this Page")


# buy institute notes
login_required(login_url='login')
def buyInstituteNotes(request, id):
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
                return render(request, 'buy/buy_institute_note.html', context={'note': note})
        elif request.method == "POST":
            data = BuyInstituteNotes.objects.create(
                student=student,
                status=1,
                note=note
            )

            request.session['owner'] = note.institute.user
            request.session['customer'] = user
            request.session['price'] = note.price
            request.session['product'] = note.title
            request.session['category'] = 'Notes'

            try:
                data.save()
                revenue(request)
                return redirect('notesstudents')
            except:
                errors.append("Some error Occured! Try Again")
                context['errors'] = errors
                return redirect('notesstudents')
        return HttpResponse("Unknown error")
    return HttpResponse("You are Not Authenticated for this page")


# buy tutor notes
login_required(login_url='login')
def buyTutorNotes(request, id):
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
                return render(request, 'buy/buy_tutor_note.html', context={'note': note})
        elif request.method == "POST":
            data = BuyTutorNotes.objects.create(
                student=student,
                status=1,
                note=note
            )

            request.session['owner'] = note.tutor.user
            request.session['customer'] = user
            request.session['price'] = note.price
            request.session['product'] = note.title
            request.session['category'] = 'Notes'

            try:
                data.save()
                revenue(request)
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
                return render(request, 'buy/buy_tutor_tutorial.html', context={'tutorial': tutorial})
        elif request.method == "POST":
            data = BuyTutorTutorial.objects.create(
                student=student,
                status=1,
                tutorial=tutorial
            )

            request.session['owner'] = tutorial.Tutor
            request.session['customer'] = user
            request.session['price'] = tutorial.Discounted_price
            request.session['product'] = tutorial.Title
            request.session['category'] = 'Tutorial'

            try:
                data.save()
                revenue(request)
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
                return render(request, 'buy/buy_Institute_tutorial.html', context={'tutorial': tutorial})
        elif request.method == "POST":
            data = BuyInstituteTutorial.objects.create(
                student=student,
                status=1,
                tutorial=tutorial
            )

            request.session['owner'] = tutorial.Course.institute
            request.session['customer'] = user
            request.session['price'] = tutorial.Discounted_price
            request.session['product'] = tutorial.Title
            request.session['category'] = 'Tutorial'
            try:
                data.save()
                revenue(request)
                return redirect('searchcourses')
            except:
                errors.append("Some error Occured! Try Again")
                context['errors'] = errors
                return redirect('searchcourses')
        return HttpResponse("Unknown error")
    return HttpResponse("You are Not Authenticated for this page")


login_required(login_url='login')
def buyTutorExam(request, id):
    errors = []
    if request.session['type'] == 'Student':
        user = User.objects.get(username=request.session['user'])
        student = Student.objects.get(user=user)
        exam = TutorExam.objects.get(id=id)
        if request.method == "GET":
            if int(exam.price) == 0:
                data = BuyTutorExam.objects.create(
                    student=student,
                    status=1,
                    exam=exam
                )
                try:
                    data.save()
                    return redirect('studentexams')
                except:
                    errors.append("Some error Occured! Try Again")
                    context['errors'] = errors
                    return redirect('studentexams')
            else:
                return render(request, 'buy/buy_Tutor_Exam.html', context={'exam': exam})
        elif request.method == "POST":
            data = BuyTutorExam.objects.create(
                student=student,
                status=1,
                exam=exam
            )

            request.session['owner'] = exam.tutor
            request.session['customer'] = user
            request.session['price'] = exam.price
            request.session['product'] = exam.Name
            request.session['category'] = 'Exam'

            try:
                data.save()
                revenue(request)
                return redirect('studentexams')
            except:
                errors.append("Some error Occured! Try Again")
                context['errors'] = errors
                return redirect('studentexams')
        return HttpResponse("Unknown error")
    return HttpResponse("You are Not Authenticated for this page")


login_required(login_url='login')
def revenue(request):
    owner = request.session['owner']
    customer = request.session['customer']

    json_datetime = requests.get('http://worldtimeapi.org/api/ip')
    json_datetime = json.loads(json_datetime.content)
    match_date = re.search(r'\d{4}-\d{2}-\d{2}', json_datetime['datetime'])
    match_time = re.search(r'\d{2}:\d{2}:\d{2}', json_datetime['datetime'])
    date = datetime.strptime(match_date.group()+' ' +
                             match_time.group(), '%Y-%m-%d %H:%M:%S')

    price = request.session['price']
    product = request.session['product']
    category = request.session['category']

    Revenue.objects.create(owner=owner, customer=customer,
                           date=date, price=price, product=product, category=category)

    del request.session['owner']
    del request.session['customer']
    del request.session['price']
    del request.session['product']
    del request.session['category']


login_required(login_url='login')
def revenueShow(request):
    daily_earnings = Revenue.objects.filter(owner=request.user)
    monthly_earnings = []
    yearly_earnings = []

    if request.method == 'POST':
        daily_earnings = daily_earnings.filter(
            date__range=[request.POST['start_date'], request.POST['end_date']])

    if daily_earnings:
        start_month = daily_earnings.earliest('date').date.strftime('%m')
        end_month = daily_earnings.latest('date').date.strftime('%m')

        start_year = daily_earnings.earliest('date').date.strftime('%Y')
        end_year = daily_earnings.latest('date').date.strftime('%Y')

        month = int(start_month)

        for year in range(int(start_year), int(end_year)+1):
            while month < 13:
                month_string = "{:02d}".format(month)

                monthly = daily_earnings.filter(
                    date__year=year, date__month=month)
                if monthly:
                    monthly_earnings.append(
                        [monthly[0].date, monthly.aggregate(Sum('price'))])

                if (month, year) == (int(end_month), int(end_year)):
                    break
                month += 1
            month = 1

        for year in range(int(start_year), int(end_year)+1):
            yearly = daily_earnings.filter(date__year=year)
            if yearly:
                yearly_earnings.append(
                    [yearly[0].date, yearly.aggregate(Sum('price'))])

    if request.method == 'POST':
        return render(request, 'buy/earnings_table.html', {'daily_earnings': daily_earnings, 'monthly_earnings': monthly_earnings, 'yearly_earnings': yearly_earnings})

    if request.session['type'] == "Institute":
        return render(request, 'buy/earnings.html', {'template': 'dashboard/base.html', 'daily_earnings': daily_earnings, 'monthly_earnings': monthly_earnings, 'yearly_earnings': yearly_earnings})

    elif request.session['type'] == "Teacher":
        return render(request, 'buy/earnings.html', {'template': 'dashboard/Tutor-dashboard.html', 'daily_earnings': daily_earnings, 'monthly_earnings': monthly_earnings, 'yearly_earnings': yearly_earnings})

    else:
        return HttpResponse("You Are Not Authenticated for this Page")
