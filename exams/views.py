from django.shortcuts import render,redirect,HttpResponse,HttpResponseRedirect
from accounts.models import Institute,Student,Teacher
from courses.models import Courses
from batches.models import BatchTiming,BatchTimingTutor
from exams.models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib import messages
import datetime as dt
from datetime import datetime,timedelta
from django.views.decorators.csrf import csrf_protect,csrf_exempt
from teacher.models import enrollTutors
from django.db.models import Q
from students.models import *
from itertools import chain
from dateutil import parser,rrule
import os
import json
# Create your views here.

@login_required(login_url="Login")
def AddExam(request):
    try:
        if request.session['type'] == "Institute":
            user = User.objects.get(username=request.session['user'])
            inst = Institute.objects.get(user=user)
            courses = Courses.objects.filter(intitute=inst)
            batch = BatchTiming.objects.filter(institute=inst)
            context ={
            'courses':courses,
            'batch':batch
            }
            if request.method == "POST":
                course = request.POST.get('course','')
                course = Courses.objects.get(id=course)
                classes = request.POST.get('class','')
                Batch = request.POST.get('batch','')
                name = request.POST.get('examname','')
                date = request.POST.get('date','')
                date = datetime.strptime(date, "%Y-%m-%d")
                exam_time = request.POST.get('exam_time','')
                timezone_offset = request.POST.get('timezone_offset','')
                duration = request.POST.get('duration','')
                pp = request.POST.get('pp','')
                redate = request.POST.get('redate','')
                calculator = request.POST.get('calculator','')
                imguplod = request.POST.get('imguplod','')
                nm = request.POST.get('nm','')
                negative_marks = request.POST.get('negative_marks','')
                tc = request.POST.get('tc','')
                status = request.POST.get('status','')
                noquestions = request.POST.get('noquestions','')
                print(course,classes,Batch,name,date,exam_time,timezone_offset,
                    duration,pp,noquestions,status,redate,tc,calculator,nm,imguplod,negative_marks)
                data = Exam()
                data.institute = inst
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
                messages.success(request,"Exam Added Successfully")
                return redirect("viewexams")
            return render(request,'Exam/addExam.html',context)
        return HttpResponse("You Are not Authenticated User for this Page")
    except:
        return HttpResponse("Something Unexpected")


@login_required(login_url="Login")
def ListExams(request):
    try:
        if request.session['type'] == "Institute":
            user = User.objects.get(username=request.session['user'])
            inst = Institute.objects.get(user=user)
            context = {}
            if Exam.objects.filter(institute=inst).exists():
                exams = Exam.objects.filter(institute=inst)
                context['exams']=exams
            return render(request,'Exam/viewExams.html',context)
        return HttpResponse("You Are not Authenticated User for this Page")
    except:
        return HttpResponse("Something Unexpected")



@login_required(login_url="Login")
def QuestionsSection(request):
    try:
        if request.session["type"] == "Institute":
            user = User.objects.get(username=request.session['user'])
            inst = Institute.objects.get(user=user)
            context = {}
            if Exam.objects.filter(institute=inst).exists():
                exams = Exam.objects.filter(institute=inst)
                context['exams']=exams
            else:
                context['exams']=[]
            if request.method=='POST':
                e_id = request.POST.get('exam','')
                print(request.POST)
                if  e_id:
                    print('e_id---',e_id)
                    return redirect('questions',e_id)
            return render(request,'Exam/Questionsection.html',context)
        return HttpResponse("You Are not Authenticated User for this Page")
    except:
        return HttpResponse("Something Unexpected")


@login_required(login_url="Login")
def EditExamQuestions(request):
    try:
        if request.session["type"] == "Institute":
            user = User.objects.get(username=request.session['user'])
            inst = Institute.objects.get(user=user)
            context = {}
            if Exam.objects.filter(institute=inst).exists():
                exams = Exam.objects.filter(institute=inst)
                context['exams']=exams
            else:
                context['exams']=[]
            return render(request,'Exam/editexamquestions.html',context)
        return HttpResponse("You Are not Authenticated User for this Page")
    except:
        return HttpResponse("Something Unexpected")



def FindClases(request):
    cid = request.GET.get('course_id')
    print('cid---',cid)
    if cid:
        subCategories = Courses.objects.get(id=cid)
        sub_list = []
        for sub in subCategories.forclass.split(","):
            data = {}
            data['value'] = sub
            data['text'] = sub
            print('data---',data)
            sub_list.append(data)
            print('sub_list---',sub_list)
        return JsonResponse({'sub_categories':sub_list})


@login_required(login_url="Login")
def deleteExam(request,exam_id):
    try:
        if request.session['type']=="Institute" or request.session['type']=="Teacher":
            try:
                exam = Exam.objects.get(id=exam_id)
            except:
                return HttpResponse("Unable to delete")
            if request.session['type']=="Institute":
                user = User.objects.get(username=request.session['user'])
                inst = Institute.objects.get(user=user)
                if exam.institute==inst:
                    exam.delete()
                    messages.success(request,"Exam Deleted Successfully")
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                else:
                    return HttpResponse("You Are not Authenticated User for this Action")
            else:
                if request.session['type']=="Teacher":
                    user = User.objects.get(username=request.session['user'])
                    tutor = Teacher.objects.get(user=user)
                    instTutor = enrollTutors.objects.get(teacher=tutor)
                    INSTcourse = instTutor.courseName.replace(";",'')
                    coursesID = list(set(INSTcourse))
                    courses = []
                    for i in coursesID:
                        try:
                            course = Courses.objects.get(id=int(i))
                            courses.append(course)
                        except:
                            pass
                    if exam.institute==instTutor.institute:
                        if exam.course in courses:
                            exam.delete()
                            messages.success(request,"Exam deleted Successfully")
                            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                        else:
                            return HttpResponse("You Are not Authenticated User for this Action")
                    else:
                        return HttpResponse("You Are not Authenticated User for this Action")
        return HttpResponse("You Are not Authenticated User for this Page")
    except:
        return HttpResponse("Something Unexpected")




@login_required(login_url="Login")
def Editexam(request,exam_id):
    try:
        if request.session['type']=="Institute" or request.session['type']=="Teacher":
            user = User.objects.get(username=request.session['user'])
            try:
                exam = Exam.objects.get(id=exam_id)
            except:
                return HttpResponse("Unable to edit")
            if request.session['type']=="Institute":
                inst = Institute.objects.get(user=user)
                courses = Courses.objects.filter(intitute=inst)
                batch = BatchTiming.objects.filter(institute=inst)
                context = {
                'courses':courses,
                'exam':exam,
                'batch':batch,
                'template':'dashboard/base.html'
                }
            elif request.session['type']=="Teacher":
                tutor = Teacher.objects.get(user=user)
                instTutor = enrollTutors.objects.get(teacher=tutor)
                INSTcourse = instTutor.courseName.replace(";",'')
                coursesID = list(set(INSTcourse))
                courses = []
                for i in coursesID:
                    try:
                        course = Courses.objects.get(id=int(i))
                        courses.append(course)
                    except:
                        pass
                if exam.institute==instTutor.institute:
                    if exam.course in courses:
                        batch = BatchTiming.objects.filter(institute=instTutor.institute)
                        context = {
                        'courses':courses,
                        'exam':exam,
                        'batch':batch,
                        'template':'dashboard/Tutor-dashboard.html'
                        }
                    else:
                        return HttpResponse("You Are Not Authenticated for this Page")
                else:
                    return HttpResponse("You Are Not Authenticated for this Page")
            if request.method == "POST":
                course = request.POST.get('course','')
                classes = request.POST.get('class','')
                Batch = request.POST.get('batch','')
                name = request.POST.get('examname','')
                date = request.POST.get('date','')
                exam_time = request.POST.get('exam_time','')
                timezone_offset = request.POST.get('timezone_offset','')
                duration = request.POST.get('duration','')
                pp = request.POST.get('pp','')
                redate = request.POST.get('redate','')
                calculator = request.POST.get('calculator','')
                imguplod = request.POST.get('imguplod','')
                nm = request.POST.get('nm','')
                negative_marks = request.POST.get('negative_marks','')
                tc = request.POST.get('tc','')
                status = request.POST.get('status','')
                noquestions = request.POST.get('noquestions','')
                print(course,classes,Batch,name,date,exam_time,timezone_offset,
                    duration,pp,noquestions,status,redate,tc,calculator,nm,imguplod,negative_marks)
                if course:
                    course = Courses.objects.get(id=course)
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
                messages.success(request,"Exam Updated successfully")
                if request.session['type']=="Institute":
                    return redirect('viewexams')
                elif request.session['type']=="Teacher":
                    return redirect('viewexamstutor')
            return render(request,'Exam/editExam.html',context)
        return HttpResponse("You Are not Authenticated User for this Page")
    except:
        return HttpResponse("Something Unexpected")



@login_required(login_url="Login")
def ToggleExam(request,exam_id):
    if request.session['type']=="Institute" or request.session['type']=="Teacher":
        exam = Exam.objects.get(id=exam_id)
        if request.session['type']=="Institute":
            user = User.objects.get(username=request.session['user'])
            inst = Institute.objects.get(user=user)
            if exam.status == True:
                if exam.institute == inst:
                    exam.status = False
                else:
                    return HttpResponse("You Are not Authenticated User for this Action")
                messages.success(request,"Exam Activated Successfully")
            else:
                if exam.institute == inst:
                    exam.status = True
                else:
                    return HttpResponse("You Are not Authenticated User for this Action")
                messages.warning(request,"Exam Deactivated Successfully")
            exam.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        elif request.session['type']=="Teacher":
            user = User.objects.get(username=request.session['user'])
            tutor = Teacher.objects.get(user=user)
            if enrollTutors.objects.filter(teacher=tutor).exists():
                instTutor = enrollTutors.objects.get(teacher=tutor)
                INSTcourse = instTutor.courseName.replace(";",'')
                coursesID = list(set(INSTcourse))
                courses = []
                for i in coursesID:
                    try:
                        course = Courses.objects.get(id=int(i))
                        courses.append(course)
                    except:
                        pass
                if exam.status == True:
                    if instTutor.institute == exam.institute:
                        if exam.course in courses:
                            exam.status = False
                        else:
                            return HttpResponse("You Are not Authenticated User for this Action")
                    else:
                        return HttpResponse("You Are not Authenticated User for this Action")
                    messages.success(request,"Exam Activated Successfully")
                else:
                    if instTutor.institute == exam.institute:
                        if exam.course in courses:
                            exam.status = True
                        else:
                            return HttpResponse("You Are not Authenticated User for this Action")
                    else:
                        return HttpResponse("You Are not Authenticated User for this Action")
                    messages.warning(request,"Exam Deactivated Successfully")
                    exam.save()
                    print("exam status--",exam.status)
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                return HttpResponse("You Are not an Authenticated Teacher")
    return HttpResponse("You Are not Authenticated User for this Page")



@login_required(login_url="Login")
def CreateQuestions(request,exam_id):
    if request.session['type']=="Institute" or request.session['type']=="Teacher":
        if request.session['type']=="Institute":
            user = User.objects.get(username=request.session['user'])
            inst = Institute.objects.get(user=user)
            template = "dashboard/base.html"
        elif request.session['type']=="Teacher":
            user = User.objects.get(username=request.session['user'])
            tutor = Teacher.objects.get(user=user)
            if enrollTutors.objects.filter(teacher=tutor).exists():
                INSTtutor = enrollTutors.objects.get(teacher=tutor)
                template  = 'dashboard/Tutor-dashboard.html'
            else:
                return HttpResponse("You are not Authenticated for this Page")
        errors = []
        try:
            exam = Exam.objects.get(id=exam_id)
        except:
            return HttpResponse("Unable to Add Question In this exam")
        if request.method=="POST":
            if request.session['type']=="Institute" and exam.institute == inst:
                question_type = request.POST.get('question_type',"")
                question = request.POST.get('question',"")
                solution = request.POST.get('solution',"")
                marks = request.POST.get('marks',"")
                section = request.POST.get('section',"")
                negative_marks = request.POST.get('negative_marks',"")
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
                        errors.append('Options Cannot be Empty')

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
                        errors.append('Options Cannot be Empty')
                elif question_type=='mc':
                    try:

                        options = request.POST.getlist('options','')
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
                        errors.append('Options Cannot be Empty')
                    if options:
                        for option in options:
                            answer = MultipleAnswer(
                                question = MultipleQuestion.objects.get(id=data.id),
                                option = option
                                )
                            answer.save()
                    else:
                        errors.append('Options Cannot be Empty')
                else:
                    try:
                        options = request.POST.getlist('options','')
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
                        print(e)
                        errors.append('Something Went Wrong! Try Again')
            elif request.session['type']=="Teacher" and exam.institute == INSTtutor.institute:
                question_type = request.POST.get('question_type',"")
                question = request.POST.get('question',"")
                solution = request.POST.get('solution',"")
                marks = request.POST.get('marks',"")
                section = request.POST.get('section',"")
                negative_marks = request.POST.get('negative_marks',"")
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
                        errors.append('Options Cannot be Empty')

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
                        errors.append('Options Cannot be Empty')
                elif question_type=='mc':
                    try:

                        options = request.POST.getlist('options','')
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
                        errors.append('Options Cannot be Empty')
                    if options:
                        for option in options:
                            answer = MultipleAnswer(
                                question = MultipleQuestion.objects.get(id=data.id),
                                option = option
                                )
                            answer.save()
                    else:
                        errors.append('Options Cannot be Empty')
                else:
                    try:
                        options = request.POST.getlist('options','')
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
                        print(e)
                        errors.append('Something Went Wrong! Try Again')

        shortquestions = ShortAnswerQuestion.objects.filter(exam=exam_id)
        booleanquestions = BooleanQuestion.objects.filter(exam=exam_id)
        longquestions = LongAnswerQuestion.objects.filter(exam=exam_id)
        multiplequestions = MultipleQuestion.objects.filter(exam=exam_id)
        context = {
        'exam':exam,
        'SectionA':[],
        'SectionB':[],
        'SectionC':[],
        'SectionD':[],
        'errors':errors,
        'template':template
        }
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
                context[f'Section{i}'].append(item)
                x+=1
            for item in query2:
                item.question_no = x
                item.save()
                context[f'Section{i}'].append(item)
                x+=1
            for item in query3:
                item.question_no = x
                item.save()
                context[f'Section{i}'].append(item)
                x+=1
            for item in query4:
                item.question_no = x
                item.save()
                context[f'Section{i}'].append(item)
                x+=1
        return render(request,'Exam/Questions.html',context)
    return HttpResponse("You Are not Authenticated User for this Page")



@login_required(login_url="Login")
def EditQuestions(request,exam_id):
    if request.session['type']=="Institute" or request.session['type']=="Teacher":
        errors =[]
        try:
            exam = Exam.objects.get(id=exam_id)
        except:
            return HttpResponse("Unable To Edit")
        user = User.objects.get(username=request.session['user'])
        if request.session['type']=="Institute":
            inst = Institute.objects.get(user=user)
            if exam.institute == inst:
                shortquestions = ShortAnswerQuestion.objects.filter(exam=exam_id)
                booleanquestions = BooleanQuestion.objects.filter(exam=exam_id)
                longquestions = LongAnswerQuestion.objects.filter(exam=exam_id)
                multiplequestions = MultipleQuestion.objects.filter(exam=exam_id)
                context = {
                'exam':exam,
                'SectionA':[],
                'SectionB':[],
                'SectionC':[],
                'SectionD':[],
                'errors':errors,
                'template':"dashboard/base.html"
                }
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
                        context[f'Section{i}'].append(item)
                        x+=1
                    for item in query2:
                        item.question_no = x
                        item.save()
                        context[f'Section{i}'].append(item)
                        x+=1
                    for item in query3:
                        item.question_no = x
                        item.save()
                        context[f'Section{i}'].append(item)
                        x+=1
                    for item in query4:
                        item.question_no = x
                        item.save()
                        context[f'Section{i}'].append(item)
                        x+=1
            else:
                return HttpResponse("You Are Not Authenticated for this Action")
        elif request.session['type']=="Teacher":
            tutor = Teacher.objects.get(user=user)
            if enrollTutors.objects.filter(teacher=tutor).exists():
                INSTtutor = enrollTutors.objects.get(teacher=tutor)
                if exam.institute == INSTtutor.institute:
                    shortquestions = ShortAnswerQuestion.objects.filter(exam=exam_id)
                    booleanquestions = BooleanQuestion.objects.filter(exam=exam_id)
                    longquestions = LongAnswerQuestion.objects.filter(exam=exam_id)
                    multiplequestions = MultipleQuestion.objects.filter(exam=exam_id)
                    context = {
                    'exam':exam,
                    'SectionA':[],
                    'SectionB':[],
                    'SectionC':[],
                    'SectionD':[],
                    'errors':errors,
                    'template':"dashboard/Tutor-dashboard.html"
                    }
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
                            context[f'Section{i}'].append(item)
                            x+=1
                        for item in query2:
                            item.question_no = x
                            item.save()
                            context[f'Section{i}'].append(item)
                            x+=1
                        for item in query3:
                            item.question_no = x
                            item.save()
                            context[f'Section{i}'].append(item)
                            x+=1
                        for item in query4:
                            item.question_no = x
                            item.save()
                            context[f'Section{i}'].append(item)
                            x+=1
                else:
                    return HttpResponse("You Are Not Authenticated for this Page")
            else:
                return HttpResponse("You are not Authenticated for this Page")
        return render(request,'Exam/editquestions.html',context)
    return HttpResponse("You Are not Authenticated User for this Page")



@login_required(login_url="Login")
def EditShortQuestions(request,question_id):
    if request.session['type']=="Institute" or request.session['type']=="Teacher":
        errors =[]
        try:
            question = ShortAnswerQuestion.objects.get(id=question_id)
        except:
            return HttpResponse("Unable to edit")
        if request.session['type']=="Institute":
            user = User.objects.get(username=request.session['user'])
            inst = Institute.objects.get(user=user)
            if question.exam.institute == inst:
                context={
                'question':question,
                'template':"dashboard/base.html",
                }
            else:
                return HttpResponse("You are not Authenticated for this page")
        elif request.session['type']=="Teacher":
            user = User.objects.get(username=request.session['user'])
            tutor = Teacher.objects.get(user=user)
            if enrollTutors.objects.filter(teacher=tutor).exists():
                INSTtutor = enrollTutors.objects.get(teacher=tutor)
                if question.exam.institute == INSTtutor.institute:
                    context={
                    'question':question,
                    'template':"dashboard/Tutor-dashboard.html"
                    }
                else:
                    return HttpResponse("You are not Authenticated for this page")
            else:
                return HttpResponse("You are not Authenticated for this Page")
        if request.method == "POST":
            section = request.POST.get("section","")
            marks = request.POST.get("marks","")
            nm= request.POST.get("nm","")
            negative_marks = request.POST.get("negative_marks","")
            Question = request.POST.get("question","")
            Solution = request.POST.get("solution","")
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
            except:
                errors.append('Error Occured! Try Again')

            context={
            'question':question,
            'errors':errors
            }
            return redirect("editquestions",question.exam.id)
        return render(request,'Exam/editshortquestions.html',context)
    return HttpResponse("You Are not Authenticated User for this Page")


@login_required(login_url="Login")
def DeleteShortQuestions(request,question_id):
    if request.session['type']=="Institute" or request.session['type']=="Teacher":
        errors =[]
        try:
            question = ShortAnswerQuestion.objects.get(id=question_id)
        except:
            return HttpResponse('Error Processing Request!')
        if request.session['type']=="Institute":
            user = User.objects.get(username=request.session['user'])
            inst = Institute.objects.get(user=user)
            if question.exam.institute == inst:
                question.delete()
                messages.success(request,"Question Deleted Successfully")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                return HttpResponse("You are not Authenticated for this page")
        elif request.session['type']=="Teacher":
            user = User.objects.get(username=request.session['user'])
            tutor = Teacher.objects.get(user=user)
            if enrollTutors.objects.filter(teacher=tutor).exists():
                INSTtutor = enrollTutors.objects.get(teacher=tutor)
                if question.exam.institute == INSTtutor.institute:
                    question.delete()
                    messages.success(request,"Question Deleted Successfully")
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                else:
                    return HttpResponse("You are not Authenticated for this page")
            else:
                return HttpResponse("You are not Authenticated for this Page")
    return HttpResponse("You Are not Authenticated User for this Page")



@login_required(login_url="Login")
def EditLongQuestions(request,question_id):
    if request.session['type']=="Institute" or request.session['type']=="Teacher":
        errors =[]
        try:
            question = LongAnswerQuestion.objects.get(id=question_id)
        except:
            return HttpResponse('Error Processing Request!')
        if request.session['type']=="Institute":
            user = User.objects.get(username=request.session['user'])
            inst = Institute.objects.get(user=user)
            if question.exam.institute == inst:
                context={
                'question':question,
                'template':"dashboard/base.html",
                }
            else:
                return HttpResponse("You are not Authenticated for this page")
        elif request.session['type']=="Teacher":
            user = User.objects.get(username=request.session['user'])
            tutor = Teacher.objects.get(user=user)
            if enrollTutors.objects.filter(teacher=tutor).exists():
                INSTtutor = enrollTutors.objects.get(teacher=tutor)
                if question.exam.institute == INSTtutor.institute:
                    context={
                    'question':question,
                    'template':"dashboard/Tutor-dashboard.html",
                    }
                else:
                    return HttpResponse("You are not Authenticated for this page")
            else:
                return HttpResponse("You are not Authenticated for this Page")
        if request.method == "POST":
            section = request.POST.get("section","")
            marks = request.POST.get("marks","")
            nm= request.POST.get("nm","")
            negative_marks = request.POST.get("negative_marks","")
            Question = request.POST.get("question","")
            Solution = request.POST.get("solution","")
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
            except:
                errors.append('Error Occured! Try Again')
            context={
            'question':question,
            'errors':errors
            }
            return redirect("editquestions",question.exam.id)
        return render(request,'Exam/editlongquestions.html',context)
    return HttpResponse("You Are not Authenticated User for this Page")


@login_required(login_url="Login")
def EditBooleanQuestions(request,question_id):
    if request.session['type']=="Institute" or request.session['type']=="Teacher":
        errors =[]
        try:
            question = BooleanQuestion.objects.get(id=question_id)
        except:
            return HttpResponse('Error Processing Request!')
        if request.session['type']=="Institute":
            user = User.objects.get(username=request.session['user'])
            inst = Institute.objects.get(user=user)
            if question.exam.institute == inst:
                context={
                'question':question,
                'template':"dashboard/base.html",
                }
            else:
                return HttpResponse("You are not Authenticated for this page")
        elif request.session['type']=="Teacher":
            user = User.objects.get(username=request.session['user'])
            tutor = Teacher.objects.get(user=user)
            if enrollTutors.objects.filter(teacher=tutor).exists():
                INSTtutor = enrollTutors.objects.get(teacher=tutor)
                if question.exam.institute == INSTtutor.institute:
                    context={
                    'question':question,
                    'template':"dashboard/Tutor-dashboard.html",
                    }
                else:
                    return HttpResponse("You are not Authenticated for this page")
            else:
                return HttpResponse("You are not Authenticated for this Page")
        if request.method == "POST":
            section = request.POST.get("section","")
            marks = request.POST.get("marks","")
            nm= request.POST.get("nm","")
            negative_marks = request.POST.get("negative_marks","")
            Question = request.POST.get("question","")
            Solution = request.POST.get("solution","")
            option1 = request.POST.get("option1","")
            option2 = request.POST.get("option2","")
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
            except:
                errors.append('Error Occured! Try Again')
            context={
            'question':question,
            'errors':errors
            }
            return redirect("editquestions",question.exam.id)
        return render(request,'Exam/editbooleanquestions.html',context)
    return HttpResponse("You Are not Authenticated User for this Page")



@login_required(login_url="Login")
def EditMultipleQuestions(request,question_id):
    if request.session['type']=="Institute" or request.session['type']=="Teacher":
        errors =[]
        try:
            question = MultipleQuestion.objects.get(id=question_id)
        except:
            return HttpResponse('Error Pr+ocessing Request!')
        if request.session['type']=="Institute":
            user = User.objects.get(username=request.session['user'])
            inst = Institute.objects.get(user=user)
            if question.exam.institute == inst:
                context={
                'question':question,
                'template':"dashboard/base.html",
                }
            else:
                return HttpResponse("You are not Authenticated for this page")
        elif request.session['type']=="Teacher":
            user = User.objects.get(username=request.session['user'])
            tutor = Teacher.objects.get(user=user)
            if enrollTutors.objects.filter(teacher=tutor).exists():
                INSTtutor = enrollTutors.objects.get(teacher=tutor)
                if question.exam.institute == INSTtutor.institute:
                    context={
                    'question':question,
                    'template':"dashboard/Tutor-dashboard.html",
                    }
                else:
                    return HttpResponse("You are not Authenticated for this page")
            else:
                return HttpResponse("You are not Authenticated for this Page")
        if request.method == "POST":
            section = request.POST.get("section","")
            marks = request.POST.get("marks","")
            nm= request.POST.get("nm","")
            negative_marks = request.POST.get("negative_marks","")
            Question = request.POST.get("question","")
            Solution = request.POST.get("solution","")
            options = request.POST.getlist("options","")
            print(options)
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
            if MultipleAnswer.objects.filter(question=question).exists():
                answers = MultipleAnswer.objects.filter(question=question)
                for i in range(len(options)):
                    if answers.filter(option=options[i]).exists():
                        answer = answers.get(option=options[i])
                        answer.option = options[i]
                    else:
                        data = MultipleAnswer(
                            question=question,
                            option = options[i]).save()
            context={
            'question':question,
            'errors':errors
            }
            return redirect("editquestions",question.exam.id)
        return render(request,'Exam/editmultiplequestions.html',context)
    return HttpResponse("You Are not Authenticated User for this Page")



@login_required(login_url="Login")
def DeleteLongQuestions(request,question_id):
    if request.session['type']=="Institute" or request.session['type']=="Teacher":
        errors =[]
        try:
            question = LongAnswerQuestion.objects.get(id=question_id)
        except:
            return HttpResponse('Error Processing Request!')
        if request.session['type']=="Institute":
            user = User.objects.get(username=request.session['user'])
            inst = Institute.objects.get(user=user)
            if question.exam.institute == inst:
                question.delete()
                messages.success(request,"Question Deleted Successfully")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                return HttpResponse("You are not Authenticated for this page")
        elif request.session['type']=="Teacher":
            user = User.objects.get(username=request.session['user'])
            tutor = Teacher.objects.get(user=user)
            if enrollTutors.objects.filter(teacher=tutor).exists():
                INSTtutor = enrollTutors.objects.get(teacher=tutor)
                if question.exam.institute == INSTtutor.institute:
                    question.delete()
                    messages.success(request,"Question Deleted Successfully")
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                else:
                    return HttpResponse("You are not Authenticated for this page")
            else:
                return HttpResponse("You are not Authenticated for this Page")
    return HttpResponse("You Are not Authenticated User for this Page")


@login_required(login_url="Login")
def DeleteBooleanQuestions(request,question_id):
    if request.session['type']=="Institute" or request.session['type']=="Teacher":
        errors =[]
        try:
            question = BooleanQuestion.objects.get(id=question_id)
        except:
            return HttpResponse('Error Processing Request!')
        if request.session['type']=="Institute":
            user = User.objects.get(username=request.session['user'])
            inst = Institute.objects.get(user=user)
            if question.exam.institute == inst:
                question.delete()
                messages.success(request,"Question Deleted Successfully")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                return HttpResponse("You are not Authenticated for this page")
        elif request.session['type']=="Teacher":
            user = User.objects.get(username=request.session['user'])
            tutor = Teacher.objects.get(user=user)
            if enrollTutors.objects.filter(teacher=tutor).exists():
                INSTtutor = enrollTutors.objects.get(teacher=tutor)
                if question.exam.institute == INSTtutor.institute:
                    question.delete()
                    messages.success(request,"Question Deleted Successfully")
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                else:
                    return HttpResponse("You are not Authenticated for this page")
            else:
                return HttpResponse("You are not Authenticated for this Page")
    return HttpResponse("You Are not Authenticated User for this Page")


@login_required(login_url="Login")
def DeleteMultipleQuestions(request,question_id):
    if request.session['type']=="Institute":
        errors =[]
        try:
            question = MultipleQuestion.objects.get(id=question_id)
        except:
            errors.append('Error Processing Request!')
        if request.session['type']=="Institute":
            user = User.objects.get(username=request.session['user'])
            inst = Institute.objects.get(user=user)
            if question.exam.institute == inst:
                question.delete()
                messages.success(request,"Question Deleted Successfully")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                return HttpResponse("You are not Authenticated for this page")
        elif request.session['type']=="Teacher":
            user = User.objects.get(username=request.session['user'])
            tutor = Teacher.objects.get(user=user)
            if enrollTutors.objects.filter(teacher=tutor).exists():
                INSTtutor = enrollTutors.objects.get(teacher=tutor)
                if question.exam.institute == INSTtutor.institute:
                    question.delete()
                    messages.success(request,"Question Deleted Successfully")
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                else:
                    return HttpResponse("You are not Authenticated for this page")
            else:
                return HttpResponse("You are not Authenticated for this Page")
    return HttpResponse("You Are not Authenticated User for this Page")


@login_required(login_url="Login")
def StudentExamsAll(request):
    student = Student.objects.get(user=request.user)
    statuses = []
    if AddStudentInst.objects.filter(student=student).exists():
        institutestudent = AddStudentInst.objects.get(student=student)
        institute = institutestudent.institute
        if institute:
            exams = Exam.objects.filter(institute=institute)
            context = {
                'exams':exams
            }
        return render(request,'Exam/studentExamsAll.html',context)
    return render(request,'Exam/studentExamsAll.html')
    

@login_required(login_url="Login")
def displayQuestionList(exam):
    mq = MultipleQuestion.objects.filter(
        exam=exam).values("question", "id", "marks", "negative_marks", 'section', 'correct_ans', 'question_no')
    lq = LongAnswerQuestion.objects.filter(
        exam=exam).values("question", "id", "marks", "negative_marks", 'section', 'correct_ans', 'question_no')
    sq = ShortAnswerQuestion.objects.filter(
        exam=exam).values("question", "id", "marks", "negative_marks", 'section', 'correct_ans', 'question_no')
    tof = BooleanQuestion.objects.filter(
        exam=exam).values("question", "id", "marks", "negative_marks", 'correct_ans', "option1", "option2", 'section', 'question_no')
    opts = {}
    for m in mq:
        m["examid"] = exam.id
        m["qtype"] = "objective"
        m["qmain"] = "multiple"
        m['time'] = 0
        m["extra_time"] = 0
        options = MultipleAnswer.objects.filter(
            question_id=m["id"]).values("option")
        i = 0

        for option in options:
            i += 1
            opts[f"op{i}"] = option["option"]
        m["options"] = opts
        opts = {}
    for l in lq:
        l["examid"] = exam.id
        l["qmain"] = "long"
        l['time'] = 0
        l["extra_time"] = 0
        l["qtype"] = "subjective"
        l["answerlength"] = "long"
    for s in sq:
        s['time'] = 0
        s["extra_time"] = 0
        s["examid"] = exam.id
        s["qmain"] = "short"
        s["qtype"] = "subjective"
        s["answerlength"] = "short"
    for t in tof:
        t['time'] = 0
        t["extra_time"] = 0
        t["examid"] = exam.id
        t["qmain"] = "tof"
        t["qtype"] = "objective"
        opts["op1"] = t["option1"]
        opts["op2"] = t["option2"]
        t["options"] = opts
        t.pop("option1")
        t.pop("option2")

    test = chain(mq, sq, lq, tof)
    result = list(chain(mq, sq, lq, tof))
    result = sorted(result, key=lambda i: i['question_no'])
    sectionA = 0
    sectionB = 0
    sectionC = 0
    sectionD = 0
    for q in result:
        if q['section'] == 'A':
            sectionA += 1
            q['questionNo'] = sectionA
        elif q['section'] == 'B':
            sectionB += 1
            q['questionNo'] = sectionB
        elif q['section'] == 'C':
            sectionC += 1
            q['questionNo'] = sectionC
        elif q['section'] == 'D':
            sectionD += 1
            q['questionNo'] = sectionD
    print(result)
    section = {}
    section['SectionA'] = sectionA
    section['SectionB'] = sectionB
    section['SectionC'] = sectionC
    section['SectionD'] = sectionD

    return result, section


@login_required(login_url="Login")
def calculator(request):
    return render(request, 'Exam/calculator.html')


@login_required(login_url="Login")
def instruction(request, pk):
	exam = Exam.objects.get(id=pk)
	request.session['exam_id'] = exam.id
	print(displayQuestionList(exam))
	if 'main' in request.GET:
		instructions = exam.tandc
		return render(request, 'Exam/Instruction2.html', {'exam': exam, 'instructions': instructions})
	return render(request, 'Exam/Instruction1.html', {'exam': exam})


@login_required(login_url="Login")
def start_exam(request, pk):
    if request.session['type']=="Student":
        exam_mapping = Exam.objects.get(id=pk)
        exam_duration = str(exam_mapping.exam_duration)
        calc = exam_mapping.calculator
        (result, section_count) = displayQuestionList(exam_mapping)
        data = {}
        data["questions"] = list(result)
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        exam_status = request.session.get('exam_status', 'start')
        user = User.objects.get(username=request.session['user'])
        student = Student.objects.get(user=user)
        s = StudentMapping.objects.get_or_create(
            student=student, course=exam_mapping.course,exam=exam_mapping)
        exam_duration = int(exam_duration)

        if exam_status == 'start':
            currentsession = {}
            for q in result:
                new = StudentAnswer()
                new.student = s[0]
                new.exam = exam_mapping
                new.question = q['question']
                new.marks = q['marks']
                new.correct_ans = q['correct_ans']
                new.negative_marks = q['negative_marks']
                new.qtype = q['qmain']
                new.save()

            with open(os.path.join(BASE_DIR, 'static/currentsession.json'), 'w') as out:
                json.dump(currentsession, out)
        request.session['exam_status'] = f'in exam of {pk}'
        with open(os.path.join(BASE_DIR, 'static/questions.json'), 'w') as out:
            json.dump(data, out)
        return render(request, 'Exam/quiz.html', {'data': data, 'student': student, 'exam': exam_mapping, 'exam_duration': exam_duration, 'calc': calc, 'section_count': section_count})
    return HttpResponse("You are not Authenticated for this page")


@login_required(login_url="Login")
def view_questions(request, pk):
    exam_mapping = Exam.objects.get(id=pk)
    (result, section_count) = displayQuestionList(exam_mapping)
    sectionA = 0
    sectionB = 0
    sectionC = 0
    sectionD = 0

    for q in result:
        if q['section'] == 'A':
            sectionA += 1
            q['questionNo'] = sectionA
        elif q['section'] == 'B':
            sectionB += 1
            q['questionNo'] = sectionB
        elif q['section'] == 'C':
            sectionC += 1
            q['questionNo'] = sectionC
        elif q['section'] == 'D':
            sectionD += 1
            q['questionNo'] = sectionD
    return render(request, 'Exam/view_questions.html', {'questions': result, 'exam': exam_mapping})


@login_required(login_url="Login")
def store_data(request):
    data = {}
    data['ans'] = request.POST.getlist('ans[]')
    data['timer'] = request.POST.get('timer')
    data['time'] = request.POST.getlist('time[]')
    data['extra_time'] = request.POST.getlist('extra_time[]')
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open(os.path.join(BASE_DIR, '/static/currentsession.json'), 'w') as out:
        json.dump(data, out)
    return JsonResponse({'hell': 'dd'})


@login_required(login_url="Login")
def submitted(request):
	exam_status = request.session['exam_status']
	exam_id = request.session.get('exam_id', 'kk')
	user = User.objects.get(username=request.session['user'])
	student = Student.objects.get(user=user)
	exam = Exam.objects.get(id=exam_id)
	s = StudentMapping.objects.get(student=student, exam=exam)
	student_answers = StudentAnswer.objects.filter(student=s,exam=exam)
	print(student_answers)
	for ans in student_answers:
		if ans.qtype == 'multiple' or ans.qtype == 'tof':
			if ans.input_ans != 'Not Answered':
				if ans.input_ans == ans.correct_ans:
					ans.marks_given = ans.marks
					ans.check = 'correct'
				else:
					ans.marks_given = -abs(ans.negative_marks)
					ans.check = 'incorrect'
				ans.save()
	new = StudentExamResult(exam=exam, attempted=True)
	new.student = s
	new.save()
	del request.session['exam_status']
	return render(request, 'Exam/submitted.html')


@login_required(login_url="Login")
def multiple_ans(request):
    q_id = request.POST.get('q_id')
    input_ans = request.POST.get('correct')
    examid = int(request.POST.get('examid'))
    exam = Exam.objects.get(id=examid)
    question = MultipleQuestion.objects.get(id=q_id)
    user = User.objects.get(username=request.session['user'])
    student = Student.objects.get(user=user)
    s = StudentMapping.objects.get(student=student, exam=exam)
    exist = StudentAnswer.objects.get_or_create(
        qtype='short', question=question.question, student=s,exam=exam,marks=0,negative_marks=0.0)
    print(exist)
    if len(exist)>1:
    	exist = exist[0]
    exist.input_ans = input_ans
    exist.correct_ans = question.correct_ans
    exist.time = 0.0#time
    exist.extra_time = 0.0#extra_time
    exist.save()
    return JsonResponse({'done': 'done'})



@login_required(login_url="Login")
def short_ans(request):
    q_id = request.POST.get('q_id')
    input_ans = request.POST.get('correct')
    examid = int(request.POST.get('examid'))
    #rish 
    if request.FILES.get('ans_Image'):
        ans_Image = request.FILES.get('ans_Image')
    else:
        ans_Image = False
    user = User.objects.get(username=request.session['user'])
    student = Student.objects.get(user=user)
    question = ShortAnswerQuestion.objects.get(id=q_id)
    exam = Exam.objects.get(id=examid)
    s = StudentMapping.objects.get(student=student, exam=exam)
    exist = StudentAnswer.objects.get_or_create(
        qtype='short', question=question.question, student=s,exam=exam,marks=0,negative_marks=0.0)
    print(exist)
    if len(exist)>1:
    	exist = exist[0]
    exist.input_ans = input_ans
    # rish ans image handle
    if ans_Image:
        exist.input_ans_Image = ans_Image

    exist.time = 0.0#time
    exist.extra_time = 0.0#extra_time
    exist.save()
    print('saved')
    return JsonResponse({'done': 'done'})


@login_required(login_url="Login")
def long_ans(request):
    q_id = request.POST.get('q_id')
    input_ans = request.POST.get('correct')
    examid = int(request.POST.get('examid'))
#rish 
    if request.FILES.get('ans_Image'):
        ans_Image = request.FILES.get('ans_Image')
    else:
        ans_Image = False
    user = User.objects.get(username=request.session['user'])
    student = Student.objects.get(user=user)
    question = LongAnswerQuestion.objects.get(id=q_id)
    exam = Exam.objects.get(id=examid)
    s = StudentMapping.objects.get(student=student, exam=exam)
    exist = StudentAnswer.objects.get_or_create(
        qtype='short', question=question.question, student=s,exam=exam,marks=0,negative_marks=0.0)
    print(exist)
    if len(exist)>1:
    	exist = exist[0]
    exist.input_ans = input_ans
    # rish ans image handle
    if ans_Image:
        exist.input_ans_Image = ans_Image

    exist.time = 0.0#time
    exist.extra_time = 0.0#extra_time
    exist.save()
    print('saved')
    return JsonResponse({'done': 'done'})


@login_required(login_url="Login")
@csrf_exempt
def tof_ans(request):
    q_id = request.POST.get('q_id')
    input_ans = request.POST.get('correct')
    examid = int(request.POST.get('examid'))
    question = BooleanQuestion.objects.get(id=q_id)
    user = User.objects.get(username=request.session['user'])
    student = Student.objects.get(user=user)
    exam = Exam.objects.get(id=examid)
    s = StudentMapping.objects.get(student=student, exam=exam)
    exist = StudentAnswer.objects.get_or_create(
        qtype='short', question=question.question, student=s,exam=exam,marks=0,negative_marks=0.0)
    print(exist)
    if len(exist)>1:
    	exist = exist[0]
    exist.input_ans = input_ans
    exist.time = 0.0#time
    exist.extra_time = 0.0#extra_time
    exist.save()
    print('saved')
    return JsonResponse({'done': 'done'})



@login_required(login_url="Login")
def ExamTutor(request):
    if request.session['type']=="Teacher":
        user = User.objects.get(username=request.session['user'])
        tutor = Teacher.objects.get(user=user)
        courses = []
        batch = []
        INSTtutor = []
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
            batch = BatchTiming.objects.filter(institute=INSTtutor.institute)
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
        'INSTtutor':INSTtutor,
        'courses':courses,
        'batch':batch,
        }
        if request.method == "POST":
            print(request.POST)
            course = request.POST.get('course','')
            check = request.POST.get('check','')
            course = Courses.objects.get(id=int(course))
            Class = request.POST.get('class','')
            name = request.POST.get('examname','')
            date = request.POST.get('date','')
            date = datetime.strptime(date, "%Y-%m-%d")
            exam_time = request.POST.get('exam_time','')
            timezone_offset = request.POST.get('timezone_offset','')
            duration = request.POST.get('duration','')
            pp = request.POST.get('pp','')
            redate = request.POST.get('redate','')
            calculator = request.POST.get('calculator','')
            imguplod = request.POST.get('imguplod','')
            nm = request.POST.get('nm','')
            negative_marks = request.POST.get('negative_marks','')
            tc = request.POST.get('tc','')
            status = request.POST.get('status','')
            noquestions = request.POST.get('noquestions','')
            if enrollTutors.objects.filter(teacher=tutor).exists() and check=='on':
                Batch = request.POST.get('batch','')
                INSTtutor = enrollTutors.objects.get(teacher=tutor)
                data = Exam()
                data.institute = INSTtutor.institute
                data.course = course
                data.Class = Class
                data.Batch = Batch
                data.Name = name
                data.exam_date = date
                data.exam_time = exam_time
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
                print('data----',data)
                messages.success(request,"Exam Added Successfully")
                return redirect('viewexamstutor')
            else:
                price = request.POST.get('price')
                data = TutorExam()
                data.tutor = tutor
                data.course = course
                data.Class = Class
                data.price = price
                data.Name = name
                data.exam_date = date
                data.exam_time = exam_time
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
                print('data----',data)
                messages.success(request,"Exam Added Successfully")
                return redirect('viewexamstutor')
                
        return render(request,'Exam/addExamTutor.html',context)
    return HttpResponse("You are not Authenticate for this Page")


@login_required(login_url="Login")
def ViewExamTutor(request):
    try:
        if request.session['type']=="Teacher":
            user = User.objects.get(username=request.session['user'])
            tutor = Teacher.objects.get(user=user)
            exams = []
            tutorexams = []
            if enrollTutors.objects.filter(teacher=tutor).exists():
                INSTtutor = enrollTutors.objects.get(teacher=tutor)
                INSTcourse = INSTtutor.courseName.replace(";",'')
                coursesID = list(set(INSTcourse))
                for i in coursesID:
                    course = Courses.objects.get(id=int(i))
                    exam = Exam.objects.filter(Q(institute=INSTtutor.institute) & Q(course=course))
                    exams.append(exam)
            tutorexams = TutorExam.objects.filter(tutor=tutor)
            context = {
            'INSTtutor':INSTtutor,
            'exams':exams,
            'tutorexams':tutorexams
            }
            return render(request,'Exam/viewExamsTutor.html',context)
        return HttpResponse("You are not Authenticate for this Page")
    except:
        return HttpResponse("You are not Authenticate for this Page")



@login_required(login_url="Login")
def ToggleTutorExam(request,exam_id):
    try:
        if request.session['type']=="Teacher":
            user = User.objects.get(username=request.session['user'])
            tutor = Teacher.objects.get(user=user)
            try:
                exam = TutorExam.objects.get(id=exam_id)
            except:
                return HttpResponse("Unable to toggle")
            if exam.tutor==tutor:
                if exam.status==False:
                    exam.status=True
                else:
                    exam.status=False
                exam.save()
                return redirect('viewexamstutor')
            else:
                return HttpResponse("You are not Authenticate for this Page")
        return HttpResponse("You are not Authenticate for this Page")
    except:
        return HttpResponse("You are not Authenticate for this Page")



@login_required(login_url="Login")
def DeleteTutorExam(request,exam_id):
    try:
        if request.session['type']=="Teacher":
            try:
                exam = TutorExam.objects.get(id=exam_id)
            except:
                return HttpResponse("Unable to delete")
            user = User.objects.get(username=request.session['user'])
            tutor = Teacher.objects.get(user=user)
            if exam.tutor==tutor:
                exam.delete()
                messages.success(request,"Exam Deleted Successfully")
                return redirect('viewexamstutor')
            else:
                return HttpResponse("You Are not Authenticated for this Action")
        return HttpResponse("You are not Authenticated for this Page")
    except:
        return HttpResponse("Something Unexpected")



@login_required(login_url="Login")
def EditExamTutor(request,exam_id):
    if request.session['type']=="Teacher":
        try:
            exam = TutorExam.objects.get(id=exam_id)
        except:
            return HttpResponse("Unable to edit")
        user = User.objects.get(username=request.session['user'])
        tutor = Teacher.objects.get(user=user)
        Tutorcourse = tutor.course.replace(";",'')
        coursesID = list(set(Tutorcourse))
        courses=[]
        for i in coursesID:
            try:
                course = Courses.objects.get(id=int(i))
                courses.append(course)
            except:
                pass
        context = {
                'courses':courses,
                'exam':exam
                  }    
        if request.method == "POST":
            course = request.POST.get('course','')
            classes = request.POST.get('class','')
            price = request.POST.get('price','')
            name = request.POST.get('examname','')
            date = request.POST.get('date','')
            exam_time = request.POST.get('exam_time','')
            timezone_offset = request.POST.get('timezone_offset','')
            duration = request.POST.get('duration','')
            pp = request.POST.get('pp','')
            redate = request.POST.get('redate','')
            calculator = request.POST.get('calculator','')
            imguplod = request.POST.get('imguplod','')
            nm = request.POST.get('nm','')
            negative_marks = request.POST.get('negative_marks','')
            tc = request.POST.get('tc','')
            status = request.POST.get('status','')
            noquestions = request.POST.get('noquestions','')
            if course:
                course = Courses.objects.get(id=course)
                exam.course = course
            if classes:
                exam.Class = classes
            if price:
                exam.price = price
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
            messages.success(request,"Exam Edited Successfully")
            return redirect('viewexamstutor')
        if exam.tutor == tutor:
            return render(request,'Exam/editExamTutor.html',context)
        else:
            return HttpResponse("You are Not Authenticated for this Page")
    return HttpResponse("You are Not Authenticated for this Page")
    

@login_required(login_url="Login")
def addQuestionsTutor(request):
    try:
        if request.session['type']=="Teacher":
            user = User.objects.get(username=request.session['user'])
            tutor = Teacher.objects.get(user=user)
            exams = []
            tutorexams = []
            if enrollTutors.objects.filter(teacher=tutor).exists():
                INSTtutor = enrollTutors.objects.get(teacher=tutor)
                INSTcourse = INSTtutor.courseName.replace(";",'')
                coursesID = list(set(INSTcourse))
                for i in coursesID:
                    course = Courses.objects.get(id=int(i))
                    exam = Exam.objects.filter(Q(institute=INSTtutor.institute) & Q(course=course))
                    exams.append(exam)
            tutorexams = TutorExam.objects.filter(tutor=tutor)
            context = {
            'INSTtutor':INSTtutor,
            'exams':exams,
            'tutorexams':tutorexams
            }
            return render(request,'Exam/addQuestionsTutor.html',context)
        return HttpResponse("You are not Authenticate for this Page")
    except:
        return HttpResponse("Something Unexpected")



@login_required(login_url="Login")
def CreateQuestionsTutor(request,exam_id):
    if request.session['type']=="Teacher":
        errors = []
        try:
            exam = TutorExam.objects.get(id=exam_id)
        except:
            return HttpResponse("Unable to add Question")
        user = User.objects.get(username=request.session['user'])
        tutor = Teacher.objects.get(user=user)
        if exam.tutor == tutor:
            if request.method=="POST":
                print(request.POST)
                question_type = request.POST.get('question_type',"")
                question = request.POST.get('question',"")
                solution = request.POST.get('solution',"")
                marks = request.POST.get('marks',"")
                section = request.POST.get('section',"")
                negative_marks = request.POST.get('negative_marks',"")
                hindi = request.POST.get("hinditext","")
                if hindi:
                    question=hindi
                if question_type=='sq':
                    data = TutorShortAnswerQuestion(
                            exam=exam,
                            question=question,
                            correct_ans=solution,
                            marks=marks,
                            section=section)
                    if negative_marks:
                        data.negative_marks = negative_marks
                    else:
                        data.negative_marks = 0.0
                    data.save()
                elif question_type=='lq':
                    try:
                        data = TutorLongAnswerQuestion(
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
                        errors.append('Options Cannot be Empty')
                elif question_type=='mc':
                    try:

                        options = request.POST.getlist('options','')
                        print(options)
                        data = TutorMultipleQuestion(
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
                        errors.append('Options Cannot be Empty')
                    if options:
                        for option in options:
                            answer = MultipleAnswer(
                                question = MultipleQuestion.objects.get(id=data.id),
                                option = option
                                )
                            answer.save()
                    else:
                        errors.append('Options Cannot be Empty')
                else:
                    try:
                        options = request.POST.getlist('options','')
                        print(options)
                        bexam = TutorBooleanQuestion(
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
                        print(e)
                        errors.append('Something Went Wrong! Try Again')
            shortquestions = TutorShortAnswerQuestion.objects.filter(exam=exam_id)
            booleanquestions = TutorBooleanQuestion.objects.filter(exam=exam_id)
            longquestions = TutorLongAnswerQuestion.objects.filter(exam=exam_id)
            multiplequestions = TutorMultipleQuestion.objects.filter(exam=exam_id)
            context = {
            'exam':exam,
            'SectionA':[],
            'SectionB':[],
            'SectionC':[],
            'SectionD':[],
            'errors':errors
            }
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
                    context[f'Section{i}'].append(item)
                    x+=1
                for item in query2:
                    item.question_no = x
                    item.save()
                    context[f'Section{i}'].append(item)
                    x+=1
                for item in query3:
                    item.question_no = x
                    item.save()
                    context[f'Section{i}'].append(item)
                    x+=1
                for item in query4:
                    item.question_no = x
                    item.save()
                    context[f'Section{i}'].append(item)
                    x+=1
            return render(request,'Exam/QuestionsTutor.html',context)
        return HttpResponse("You Are Not Authenticated for this Page")
    return HttpResponse("You Are Not Authenticated for this Page")



@login_required(login_url="Login")
def EditExamQuestionsTutor(request):
    if request.session['type']=="Teacher":
        user = User.objects.get(username=request.session['user'])
        tutor =Teacher.objects.get(user=user)
        exams = []
        try:
            if enrollTutors.objects.filter(teacher=tutor).exists():
                INSTtutor = enrollTutors.objects.get(teacher=tutor)
                INSTcourse = INSTtutor.courseName.replace(";",'')
                coursesID = list(set(INSTcourse))
                for i in coursesID:
                    course = Courses.objects.get(id=int(i))
                    exam = Exam.objects.filter(Q(institute=INSTtutor.institute) & Q(course=course))
                    exams.append(exam)
        except:
            pass
        tutorexams = TutorExam.objects.filter(tutor=tutor)
        context = {
            'INSTtutor':INSTtutor,
            'exams':exams,
            'tutorexams':tutorexams
            }
        return render(request,'Exam/editExamQuestionsTutor.html',context)
    return HttpResponse("You are not Authenticated for this Page")



@login_required(login_url="Login")
def EditQuestionsTutor(request,exam_id):
    if request.session['type']=="Teacher":
        errors =[]
        try:
            exam = TutorExam.objects.get(id=exam_id)
        except:
            return HttpResponse("You are not Authenticated for this Page")
        user = User.objects.get(username=request.session['user'])
        tutor = Teacher.objects.get(user=user)
        if exam.tutor == tutor:
            shortquestions = TutorShortAnswerQuestion.objects.filter(exam=exam_id)
            booleanquestions = TutorBooleanQuestion.objects.filter(exam=exam_id)
            longquestions = TutorLongAnswerQuestion.objects.filter(exam=exam_id)
            multiplequestions = TutorMultipleQuestion.objects.filter(exam=exam_id)
            context = {
            'exam':exam,
            'SectionA':[],
            'SectionB':[],
            'SectionC':[],
            'SectionD':[],
            'errors':errors
            }
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
                    context[f'Section{i}'].append(item)
                    x+=1
                for item in query2:
                    item.question_no = x
                    item.save()
                    context[f'Section{i}'].append(item)
                    x+=1
                for item in query3:
                    item.question_no = x
                    item.save()
                    context[f'Section{i}'].append(item)
                    x+=1
                for item in query4:
                    item.question_no = x
                    item.save()
                    context[f'Section{i}'].append(item)
                    x+=1
            return render(request,'Exam/editQuestionsTutor.html',context)
        else:
            return HttpResponse("You Are Not Authenticated for this Page")
    return HttpResponse("You are not Authenticated for this page")


@login_required(login_url="Login")
def EditShortQuestionsTutor(request,question_id):
    if request.session['type']=="Teacher":
        errors =[]
        try:
            question = TutorShortAnswerQuestion.objects.get(id=question_id)
        except:
            return HttpResponse('Error Processing Request!')
        user = User.objects.get(username=request.session['user'])
        tutor = Teacher.objects.get(user=user)
        if question.exam.tutor==tutor:
            context={
            'question':question,
            }
        else:
            return HttpResponse("You are not Authenticated for this Page")
        if request.method == "POST":
            section = request.POST.get("section","")
            marks = request.POST.get("marks","")
            nm= request.POST.get("nm","")
            negative_marks = request.POST.get("negative_marks","")
            Question = request.POST.get("question","")
            Solution = request.POST.get("solution","")
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
            except:
                errors.append('Error Occured! Try Again')
            return redirect('editquestionstutor',question.exam.id)	
        return render(request,'Exam/editshortquestionstutor.html',context)
    return HttpResponse("You are not Authenticated for this Page")


@login_required(login_url="Login")
def EditLongQuestionsTutor(request,question_id):
    if request.session['type']=="Teacher":
        errors =[]
        try:
            question = TutorLongAnswerQuestion.objects.get(id=question_id)
        except:
            return HttpResponse('Error Processing Request!')
        user = User.objects.get(username=request.session['user'])
        tutor = Teacher.objects.get(user=user)
        if question.exam.tutor==tutor:
            context={
                'question':question,
                }
        else:
            return HttpResponse("You are not Authenticated for this Page")
        if request.method == "POST":
            section = request.POST.get("section","")
            marks = request.POST.get("marks","")
            nm= request.POST.get("nm","")
            negative_marks = request.POST.get("negative_marks","")
            Question = request.POST.get("question","")
            Solution = request.POST.get("solution","")
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
            except:
                errors.append('Error Occured! Try Again')
            return redirect('editquestionstutor',question.exam.id)	
        return render(request,'Exam/editlongquestionstutor.html',context)
    return HttpResponse("You are not Authenticated for this Page")


@login_required(login_url="Login")
def EditBooleanQuestionsTutor(request,question_id):
    if request.session['type']=="Teacher":
        errors =[]
        try:
            question = TutorBooleanQuestion.objects.get(id=question_id)
        except:
            return HttpResponse('Error Processing Request!')
        user = User.objects.get(username=request.session['user'])
        tutor = Teacher.objects.get(user=user)
        if question.exam.tutor==tutor:
            context={
                'question':question,
                }
        else:
            return HttpResponse("You are not Authenticated for this Page")
        if request.method == "POST":
            section = request.POST.get("section","")
            marks = request.POST.get("marks","")
            nm= request.POST.get("nm","")
            negative_marks = request.POST.get("negative_marks","")
            Question = request.POST.get("question","")
            Solution = request.POST.get("solution","")
            option1 = request.POST.get("option1","")
            option2 = request.POST.get("option2","")
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
            except:
                errors.append('Error Occured! Try Again')
            return redirect('editquestionstutor',question.exam.id)
        return render(request,'Exam/editbooleanquestionstutor.html',context)
    return HttpResponse("You are not Authenticated for this Page")



@login_required(login_url="Login")
def EditMultipleQuestionsTutor(request,question_id):
    if request.session['type']=="Teacher":
        errors =[]
        try:
            question = TutorMultipleQuestion.objects.get(id=question_id)
        except:
            return HttpResponse('Error Processing Request!')
        user = User.objects.get(username=request.session['user'])
        tutor = Teacher.objects.get(user=user)
        if question.exam.tutor==tutor:
            context={
                'question':question,
                }
        else:
            return HttpResponse("You are not Authenticated for this Page")
        if request.method == "POST":
            section = request.POST.get("section","")
            marks = request.POST.get("marks","")
            nm= request.POST.get("nm","")
            negative_marks = request.POST.get("negative_marks","")
            Question = request.POST.get("question","")
            Solution = request.POST.get("solution","")
            options = request.POST.getlist("options","")
            print(options)
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
                    else:
                        data = MultipleAnswer(
                            question=question,
                            option = options[i]
                            ).save()
            try:
                question.save()
            except:
                return HttpResponse('Error Occured! Try Again')
            return redirect('editquestionstutor',question.exam.id)
        return render(request,'Exam/editmultiplequestionstutor.html',context)
    return HttpResponse("You are not Authenticated for this Page")


@login_required(login_url="Login")
def instruction(request):
    if request.session['type']=="Student":
        user = User.objects.get(username=request.session['user'])
        student = Student.objects.get(user=user)
        statuses = []
        studentExam = []
        if AddStudentInst.objects.filter(student=student).exists():
            institutestudent = AddStudentInst.objects.filter(student=student)
            institute = Institute.objects.get(user=institutestudent[0].institute.user)
            if institute:
                exams = Exam.objects.filter(institute=institute)
                for exam in exams:
                    for cou in institutestudent:
                        course = Courses.objects.get(id=cou.courseName)
                        if exam.course==course:
                            studentExam.append(exam)
                context={
                'exams':studentExam,
                }
            return render(request,'Exam/studentExamsAll.html',context)
        return render(request,'Exam/studentExamsAll.html')
    return HttpResponse("You are not Authenticated for this Page")


def displayQuestionList(exam):
    mq = MultipleQuestion.objects.filter(
        exam=exam).values("question", "id", "marks", "negative_marks", 'section', 'correct_ans', 'question_no')
    lq = LongAnswerQuestion.objects.filter(
        exam=exam).values("question", "id", "marks", "negative_marks", 'section', 'correct_ans', 'question_no')
    sq = ShortAnswerQuestion.objects.filter(
        exam=exam).values("question", "id", "marks", "negative_marks", 'section', 'correct_ans', 'question_no')
    tof = BooleanQuestion.objects.filter(
        exam=exam).values("question", "id", "marks", "negative_marks", 'correct_ans', "option1", "option2", 'section', 'question_no')
    opts = {}
    for m in mq:
        m["examid"] = exam.id
        m["qtype"] = "objective"
        m["qmain"] = "multiple"
        m['time'] = 0
        m["extra_time"] = 0
        options = MultipleAnswer.objects.filter(
            question_id=m["id"]).values("option")
        i = 0

        for option in options:
            i += 1
            opts[f"op{i}"] = option["option"]
        m["options"] = opts
        opts = {}
    for l in lq:
        l["examid"] = exam.id
        l["qmain"] = "long"
        l['time'] = 0
        l["extra_time"] = 0
        l["qtype"] = "subjective"
        l["answerlength"] = "long"
    for s in sq:
        s['time'] = 0
        s["extra_time"] = 0
        s["examid"] = exam.id
        s["qmain"] = "short"
        s["qtype"] = "subjective"
        s["answerlength"] = "short"
    for t in tof:
        t['time'] = 0
        t["extra_time"] = 0
        t["examid"] = exam.id
        t["qmain"] = "tof"
        t["qtype"] = "objective"
        opts["op1"] = t["option1"]
        opts["op2"] = t["option2"]
        t["options"] = opts
        t.pop("option1")
        t.pop("option2")

    test = chain(mq, sq, lq, tof)
    result = list(chain(mq, sq, lq, tof))
    result = sorted(result, key=lambda i: i['question_no'])
    sectionA = 0
    sectionB = 0
    sectionC = 0
    sectionD = 0
    for q in result:
        if q['section'] == 'A':
            sectionA += 1
            q['questionNo'] = sectionA
        elif q['section'] == 'B':
            sectionB += 1
            q['questionNo'] = sectionB
        elif q['section'] == 'C':
            sectionC += 1
            q['questionNo'] = sectionC
        elif q['section'] == 'D':
            sectionD += 1
            q['questionNo'] = sectionD
    print(result)
    section = {}
    section['SectionA'] = sectionA
    section['SectionB'] = sectionB
    section['SectionC'] = sectionC
    section['SectionD'] = sectionD

    return result, section

@login_required(login_url="Login")
def instruction(request, pk):
    if request.session['type']=="Student":
        exam = Exam.objects.get(id=pk)
        request.session['exam_id'] = exam.id
        if 'main' in request.GET:
            instructions = exam.tandc
            return render(request, 'Exam/Instruction2.html', {'exam': exam, 'instructions': instructions})
        return render(request, 'Exam/Instruction1.html', {'exam': exam})