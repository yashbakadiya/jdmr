from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.decorators import login_required
from accounts.models import Institute,Teacher,Student
from exams.models import *
from students.models import AddStudentInst
from django.contrib.auth.models import User
from django.db.models import Sum
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers
from .utils import render_to_pdf
# Create your views here.

# coaching result 
@login_required(login_url="Login")
def CoachingResultStudent(request):
    if request.session['type'] == "Institute":
        user = User.objects.get(username=request.session['user'])
        inst = Institute.objects.get(user=user)
        context = {}
        if Exam.objects.filter(institute=inst).exists():
            exams = Exam.objects.filter(institute=inst)
            context['exams']=exams
        return render(request,'Results/ResultInstitute.html',context)
    return HttpResponse("You Are not Authenticated User for this Page")

@login_required(login_url="Login")
def GetExamResults(request,exam_id):
    exam = Exam.objects.get(id=exam_id)
    students = StudentMapping.objects.filter(exam=exam)
    batches = []
    for std in students:
        batches.append(AddStudentInst.objects.get(student = std.student).batch)
    context={
	'students':zip(students,batches)
	}
    return render(request,'Results/GetExamResultCenter.html',context)

@login_required(login_url="Login")
def GetStudentResults(request,student_id,exam_id):
    mapping = StudentMapping.objects.get(id=student_id)
    exam = Exam.objects.get(id=exam_id)
    student_results = StudentExamResult.objects.get(student=mapping,exam=exam)
    student_answers = StudentAnswer.objects.filter(student=mapping,exam=exam).order_by('id')
    question_no_list = []
    for que in student_answers:
        if que.qtype == 'long':
            question_no_list.append(LongAnswerQuestion.objects.get(exam=exam,question=que.question).question_no)
        elif que.qtype == 'short':
            question_no_list.append(ShortAnswerQuestion.objects.get(exam=exam,question=que.question).question_no)
        elif que.qtype == 'multiple':
            question_no_list.append(MultipleQuestion.objects.get(exam=exam,question=que.question).question_no)
        elif que.qtype == 'tof':
            question_no_list.append(BooleanQuestion.objects.get(exam=exam,question=que.question).question_no)
            
    if request.method=='POST':
        calculate(student_answers,student_results)
    context = {
	'student_answers':zip(question_no_list,student_answers),
	'status':student_results.attempted,
	'result':student_results,
	'exam':exam,
	'mapping':mapping
	}
    
    return render(request,'Results/StudentResult.html',context) 

@login_required(login_url="Login")
def Review_Answer(request,question_id):
    answer = StudentAnswer.objects.get(id=question_id)
    context={
	'answer':answer
	}
    if request.method == "POST":
        marks = request.POST.get("marks",0.0)
        answer.marks_given = marks
        answer.save()
        return redirect('studentresult',answer.student.id,answer.exam.id)
    return render(request,'Results/Review_Answer.html',context)

def giveMarks(marks):
    if marks == None:
        return 0
    else:
        return marks

def countQuestionAttributes(exam_mapping):
    for exam in exam_mapping:
        mq = MultipleQuestion.objects.filter(exam=exam)
        negativeq = mq.filter(negative_marks__lte=-0.1).count()
        multiple_marks = mq.aggregate(Sum('marks'))
        multiple_marks = giveMarks(multiple_marks['marks__sum'])
        count = mq.count()

        lq = LongAnswerQuestion.objects.filter(exam=exam)
        negativeq += lq.filter(negative_marks__lte=-0.1).count()
        long_marks = lq.aggregate(Sum('marks'))
        long_marks = giveMarks(long_marks['marks__sum'])
        count += lq.count()

        sq = ShortAnswerQuestion.objects.filter(exam=exam)
        negativeq += sq.filter(negative_marks__lte=-0.1).count()
        short_marks = sq.aggregate(Sum('marks'))
        short_marks = giveMarks(short_marks['marks__sum'])
        count += sq.count()

        tq = BooleanQuestion.objects.filter(exam=exam)
        negativeq += tq.filter(negative_marks__lte=-0.1).count()
        tof_marks = tq.aggregate(Sum('marks'))
        tof_marks = giveMarks(tof_marks['marks__sum'])
        count += tq.count()

        marks = multiple_marks + short_marks + long_marks + tof_marks
        exam.marks = marks
        exam.q_count = count
        exam.negativeq = negativeq

    return exam_mapping

@login_required(login_url="Login")
def webViewerAnnotate(request, id, pk):
    return render(request, 'Results/annotation.html',{"id":id,"pk":pk})

@login_required(login_url="Login")
def annotateAnswers(request, id, pk):
    exam_mapping = Exam.objects.filter(id=id)
    exam = exam_mapping[0]
    student = StudentMapping.objects.get(id=pk)
    name = f"{student.student.user.first_name} {student.student.user.last_name}"
    student_results = StudentAnswer.objects.filter(student=student, exam=exam)
    exam_mapping = countQuestionAttributes(exam_mapping)[0]
    try:
        one = student_results[0]
        pdf = render_to_pdf('Results/annotatable_pdf.html', {'student_results': student_results, 'one': one, 'name': name, 'status': True})
        return HttpResponse(pdf,content_type="application/pdf")
    except:
        pdf = render_to_pdf('xyz.html', {'status': False})
        return HttpResponse(pdf,content_type="application/pdf")

def checked_copies_upload(request, id, pk):
    if request.POST:
        print("yes")
        print(id,pk)
        s = StudentExamResult.objects.filter(exam=id,student=pk)
        s[0].annotated_copies = request.FILES['coppies']
        s.save()

    return HttpResponseRedirect(reverse('result'))

# student result 
@login_required(login_url="Login")
def ViewExamsResult(request):
    if request.session['type']=="Student":
        user = User.objects.get(username=request.session['user'])
        student = Student.objects.get(user=user)
        context = {}
        if StudentMapping.objects.filter(student=student).exists():
            mapping = StudentMapping.objects.get(student=student)
            context['results'] = StudentExamResult.objects.filter(student=mapping)
            
        return render(request,'Results/examResultsAll.html',context)
    return HttpResponse("You Are not Authenticated for this page")


def calculate(answers,result):
    student = answers[0]

    # Correct Question
    correct_questions = answers.filter(check='correct')
    correct_qs_count = correct_questions.count()
    if correct_qs_count == 0:
        correct_qs_marks = 0
    else:
        correct_qs_marks = correct_questions.aggregate(Sum('marks_given'))[
        'marks_given__sum']

    # Incorrect Questions
    incorrect_questions = answers.filter(check='incorrect')
    incorrect_qs_count = incorrect_questions.count()
    if incorrect_qs_count == 0:
        incorrect_qs_marks = 0
    else:
        incorrect_qs_marks = incorrect_questions.aggregate(Sum('marks_given'))[
        'marks_given__sum']

    # Question Not Answered
    q_unanswered_type = answers.filter(check='Not Answered')
    q_unanswered = q_unanswered_type.count()
    if q_unanswered == 0:
        q_unanswered_marks = 0
    else:
        q_unanswered_marks = answers.filter(
            input_ans='Not Answered').aggregate(Sum('marks'))['marks__sum']
    
    # Question Total
    result.total_questions = answers.all().count()
    result.total_marks = answers.all().aggregate(Sum('marks'))['marks__sum']
    result.marks_scored = answers.all().aggregate(Sum('marks_given'))['marks_given__sum']
    result.save()

    #percent
    result.percentage = result.marks_scored/result.total_marks
    result.percentage = result.percentage * 100

    if result.percentage >= result.exam.pass_percentage:
        result.pass_status = 1
    else:
        result.pass_status = 0
    if result.percentage<0:
        result.percentage = 0.0

    result.save()

    # Question Answered
    q_answered = result.total_questions - q_unanswered
    q_answered_marks = result.total_marks - q_unanswered_marks

    return (correct_qs_count, correct_qs_marks, incorrect_qs_count,
            incorrect_qs_marks, q_unanswered, q_unanswered_marks, q_answered,
            q_answered_marks, correct_questions, incorrect_questions, q_unanswered_type)

@login_required(login_url="Login")
def detailed_result(request, pk):
    if request.session['type']=="Student":
        result = StudentExamResult.objects.get(id=pk)
        exam = result.exam
        student = result.student
        all_results = StudentExamResult.objects.filter(exam=exam)

        # Calculate student attributes
        answers = StudentAnswer.objects.filter(student=student, exam=exam)
        if answers:
            (correct_qs_count, correct_qs_marks, incorrect_qs_count,
            incorrect_qs_marks, q_unanswered, q_unanswered_marks, q_answered,
            q_answered_marks, correct_questions, incorrect_questions, q_unanswered_type) = calculate(
                answers,result)

            # Time Calculations
            exam_duration = str(exam.exam_duration)
            extra, hr, mins = 0,int(exam_duration)//60,int(exam_duration)%60
            hr = int(hr)
            mins = int(mins)
            exam_duration = f'{hr}hr {mins}mins'
            time_taken = answers.aggregate(Sum('extra_time'))[
                'extra_time__sum'] + answers.aggregate(Sum('time'))['time__sum']
            result.time_taken = round(time_taken, 2)
            result.save()

            #  Section Wise Question
            section = {}
            alpha = ['A', 'B', 'C', 'D']
            for A in alpha:
                section_ans = answers.filter(section=f'{A}')
                section_count = section_ans.count()
                if section_count == 0:
                    section_count = 0
                    section_ans = 0
                    section_correct_count = 0
                    section_incorrect_count = 0
                    section_correct_marks = 0
                    section_incorrect_marks = 0
                    section_unanswered = 0
                    section_unanswered_marks = 0
                    percentage = 0
                    section_time = 0
                else:
                    section_correct_count, section_correct = [correct_questions.filter(section=f'{A}').count(
                    ), correct_questions.filter(section=f'{A}')]
                    if section_correct_count == 0:
                        section_correct_marks = 0
                    else:
                        section_correct_marks = section_correct.aggregate(Sum('marks_given'))[
                            'marks_given__sum']
                    section_incorrect_count, section_incorrect = [section_ans.filter(
                        check='incorrect').count(), incorrect_questions.filter(section=f'{A}')]
                    if section_incorrect_count == 0:
                        section_incorrect_marks = 0
                    else:
                        section_incorrect_marks = section_incorrect.aggregate(Sum('marks_given'))[
                            'marks_given__sum']
                    section_unanswered = q_unanswered_type.filter(
                        section=f'{A}').count()
                    if section_unanswered == 0:
                        section_unanswered_marks = 0
                    else:
                        section_unanswered_marks = q_unanswered_type.filter(
                            section=f'{A}').aggregate(Sum('marks'))['marks__sum']

                    section_total_marks = section_ans.aggregate(Sum('marks'))[
                        'marks__sum']
                    section_marks_scored = section_ans.aggregate(Sum('marks_given'))[
                        'marks_given__sum']
                    percentage = round(
                        (section_marks_scored/section_total_marks) * 100, 2)
                    if percentage<0:
                        percentage = 0.0
                    percentage = f'{percentage}%'

                    section_time = section_ans.aggregate(Sum('time'))[
                        'time__sum'] + section_ans.aggregate(Sum('extra_time'))['extra_time__sum']
                if section_incorrect_marks == None:
                    section_incorrect_marks = 0
                section[f'{A}_section_count'] = section_count
                # section[f'{A}_section_question'] = section_ans
                section[f'{A}_marks'] = section_correct_marks + section_incorrect_marks
                section[f'{A}_section_correct_count'] = section_correct_count
                section[f'{A}_section_incorrect_count'] = section_incorrect_count
                section[f'{A}_section_correct_marks'] = section_correct_marks
                section[f'{A}_section_incorrect_marks'] = section_incorrect_marks
                section[f'{A}_section_unanswered'] = section_unanswered
                section[f'{A}_section_unanswered_marks'] = section_unanswered_marks
                section[f'{A}_section_percentage'] = percentage
                section[f'{A}_section_time'] = round(section_time, 2)
            
            result.correct_qs_count = correct_qs_count
            result.correct_qs_marks = correct_qs_marks
            result.incorrect_qs_count = incorrect_qs_count
            result.incorrect_qs_marks = incorrect_qs_marks
            result.q_unanswered_marks = q_unanswered_marks
            result.q_unanswered = q_unanswered
            result.q_answered = q_answered
            result.q_answered_marks = q_answered_marks
            result.exam_duration = exam_duration
            result.time_taken = round(time_taken, 2)
            result.total_students = all_results.count()
            result.save()

            details = {}
            details['correct_qs_count'] = correct_qs_count
            details['correct_qs_marks'] = correct_qs_marks
            details['incorrect_qs_count'] = incorrect_qs_count
            details['incorrect_qs_marks'] = incorrect_qs_marks
            details['q_unanswered_marks'] = q_unanswered_marks
            details['q_unanswered'] = q_unanswered
            details['q_answered'] = q_answered
            details['q_answered_marks'] = q_answered_marks
            details['exam_duration'] = exam_duration
            details['time_taken'] = time_taken
            details['total_students'] = all_results.count()

            # Rank
            rank = all_results.order_by('-marks_scored')
            count = all_results.order_by('-marks_scored').count()
            topper = rank[0]
            i = 0
            for s in rank:
                i += 1
                people_behind = count - i
                percentile = (people_behind/count)*100
                if i == 1:
                    topper_answers = StudentAnswer.objects.filter(
                        student=topper.student, exam=topper.exam)
                    (correct_qs_count, correct_qs_marks, incorrect_qs_count,
                    incorrect_qs_marks, q_unanswered, q_unanswered_marks, q_answered,
                    q_answered_marks, correct_questions, incorrect_questions, q_unanswered_type) = calculate(
                        topper_answers,StudentExamResult.objects.filter(student=topper.student, exam=topper.exam).last())
                    topper_time_taken = topper_answers.aggregate(Sum('extra_time'))[
                        'extra_time__sum'] + topper_answers.aggregate(Sum('time'))['time__sum']
                    topper.correct_qs_count = correct_qs_count
                    topper.correct_qs_marks = correct_qs_marks
                    topper.incorrect_qs_count = incorrect_qs_count
                    topper.incorrect_qs_marks = incorrect_qs_marks
                    topper.q_unanswered_marks = q_unanswered_marks
                    topper.q_unanswered = q_unanswered
                    topper.q_answered = q_answered
                    topper.q_answered_marks = q_answered_marks
                    topper.percentile = percentile
                    topper.rank = 1
                    topper.time_taken = round(topper_time_taken, 2)
                if s.student == student:
                    result.percentile = percentile
                    break

            result.rank = i
            details['rank'] = i

            details = json.dumps(details)
            json_section = json.dumps(section)

            questions = answers
            for question in questions:
                if question.qtype == 'multiple':
                    option = MultipleQuestion.objects.get(
                        question=question.question, exam=question.exam)
                    question.multiple = option
                if question.qtype == 'tof':
                    tof = BooleanQuestion.objects.get(
                        question=question.question, exam=question.exam)
                    question.tof = tof

            t = rank.values()

            json_allresults = json.dumps(list(t), cls=DjangoJSONEncoder)
            json_result = serializers.serialize('json', [result, ])

            topper_results = StudentAnswer.objects.filter(
                student=topper.student, exam=topper.exam)
            topper_section = []
            for a in alpha:
                topper_a_marks = topper_results.filter(section=f'{a}').aggregate(
                    Sum('marks_given'))['marks_given__sum']
                if topper_a_marks is None:
                    topper_a_marks = 0
                topper_section.append(topper_a_marks)
            context = {
                'result': result,
                'section': section,
                'questions': questions,
                'topper': topper,
                'json_allresults': json_allresults,
                'json_result': json_result,
                'details': details,
                'json_section': json_section,
                'topper_section': topper_section
            }
            if 'download-pdf' in request.GET:
                download_type = request.GET.get('download-pdf')
                # Download
                pdf = render_to_pdf(f'login/conversion/{download_type}.html', context)
                if pdf:
                    print('hi')
                    response = HttpResponse(pdf, content_type='application/pdf')
                    filename = f"{result.student.student.Name} Report.pdf"
                    content = f"inline; filename={filename}"
                    download = request.GET.get("download")
                    if download:
                        content = "attachment; filename=%s" % (filename)
                    response['Content-Disposition'] = content
                    return response
                    # return render(request, f'login/conversion/{download_type}.html', context)
                return HttpResponse("Not found")

        return render(request, 'Results/detailed_result.html', context)
    return HttpResponse("You Are not Authenticated for this page")