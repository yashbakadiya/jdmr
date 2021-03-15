from django.shortcuts import render,HttpResponse
from django.contrib.auth.decorators import login_required
from accounts.models import Institute,Teacher,Student
from exams.models import *
from django.contrib.auth.models import User
from django.db.models import Sum
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers
# Create your views here.

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
        overall_percent = 0

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
                    overall_percent+=percentage
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
            
            overall_percent = overall_percent/4
            result.percentage = overall_percent
            if overall_percent >= exam.pass_percentage:
                result.pass_status = 1
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