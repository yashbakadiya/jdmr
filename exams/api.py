from django.shortcuts import render, redirect, HttpResponse
from .models import Exam, MultipleQuestion, MultipleAnswer, LongAnswerQuestion, BooleanQuestion, ShortAnswerQuestion, TutorExam, TutorMultipleQuestion, TutorBooleanQuestion, TutorMultipleAnswer, TutorLongAnswerQuestion, TutorShortAnswerQuestion
from accounts.models import Institute, Teacher
from courses.models import Courses
from django.contrib.auth.models import User
import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from .serializers import ExamSerializer, MultipleQuestionSerializer, MultipleAnswerSerializer, LongAnswerQuestionSerializer, BooleanQuestionSerializer, ShortAnswerQuestionSerializer, TutorExamSerializer, TutorMultipleQuestionSerializer, TutorBooleanQuestionSerializer, TutorLongAnswerQuestionSerializer, TutorMultipleAnswerSerializer, TutorShortAnswerQuestionSerializer
from django.core import serializers


@api_view(["POST", "GET", "PATCH", "DELETE"])
def ExamAPI(request):
    if request.method == "GET":
        exam = Exam.objects.all()
        exam = serializers.serialize('json', exam)
        return HttpResponse(exam, content_type="text/json-comment-filtered")
    data = request.data
    user = User.objects.get(username=request.user)
    institute = Institute.objects.get(user=user)
    data['institute'] = institute.pk
    courseid = data['courseID']
    course = Courses.objects.get(courseID=courseid)
    data['course'] = course.pk

    if request.session["type"] == "Institute":
        if request.method == "POST":
            exam = ExamSerializer(data=data)
            if exam.is_valid():
                exam.save()
                data['success'] = "Exam Added Successfully!"
            else:
                data['error'] = exam.errors
                return Response(data)
        elif request.method == "PATCH":
            pk = data['pk']
            exam = Exam.objects.get(pk=pk)
            exam = ExamSerializer(exam, data=data, partial=True)
            if exam.is_valid():
                exam.save()
                data['success'] = "Exam Updated Successfully!"
            else:
                data['error'] = exam.errors
                return Response(data)
        elif request.method == "DELETE":
            pk = data["pk"]
            exam = Exam.objects.get(pk=pk)
            exam.delete()
            data['success'] = "Exam Deleted Successfully"
        else:
            data['error'] = "Method is not POST"
            return Response(data)
    else:
        data['error'] = "Not an Institute Login"
        return Response(data)
    return Response(data)


@api_view(["POST", "GET", "PATCH", "DELETE"])
def MultipleQuestionAPI(request):
    if request.method == "GET":
        mq = MultipleQuestion.objects.all()
        mq = serializers.serialize('json', mq)
        return HttpResponse(mq, content_type="text/json-comment-filtered")
    data = request.data
    examid = data['examid']
    exam = Exam.objects.get(id=examid)
    data['exam'] = exam.pk

    if request.session["type"] == "Institute":
        if request.method == "POST":
            mqs = MultipleQuestionSerializer(data=data)
            if mqs.is_valid():
                mqs.save()
                data['success'] = "Multiple Quesiton Added Successfully!"
            else:
                data['error'] = mqs.errors
                return Response(data)
        elif request.method == "PATCH":
            pk = data['pk']
            mqs = MultipleQuestion.objects.get(pk=pk)
            mqs = MultipleQuestionSerializer(mqs, data=data, partial=True)
            if mqs.is_valid():
                mqs.save()
                data['success'] = "Multiple Question Updated Successfully!"
            else:
                data['error'] = mqs.errors
                return Response(data)
        elif request.method == "DELETE":
            pk = data["pk"]
            mqs = MultipleQuestion.objects.get(pk=pk)
            mqs.delete()
            data['success'] = "Multiple Question Deleted Successfully"
        else:
            data['error'] = "Method is not POST"
            return Response(data)
    else:
        data['error'] = "Not an Institute Login"
        return Response(data)
    return Response(data)


@api_view(["POST", "GET", "PATCH", "DELETE"])
def MultipleAnswerAPI(request):
    if request.method == "GET":
        ma = MultipleAnswer.objects.all()
        ma = serializers.serialize('json', ma)
        return HttpResponse(ma, content_type="text/json-comment-filtered")
    data = request.data
    questionid = data['questionid']
    question = MultipleQuestion.objects.get(id=questionid)
    data['question'] = question.pk

    if request.session["type"] == "Institute":
        if request.method == "POST":
            mas = MultipleAnswerSerializer(data=data)
            if mas.is_valid():
                mas.save()
                data['success'] = "Multiple Answers Added Successfully!"
            else:
                data['error'] = mas.errors
                return Response(data)
        elif request.method == "PATCH":
            pk = data['pk']
            mas = MultipleAnswer.objects.get(pk=pk)
            mas = MultipleAnswerSerializer(mas, data=data, partial=True)
            if mas.is_valid():
                mas.save()
                data['success'] = "Multiple Answers Updated Successfully!"
            else:
                data['error'] = mas.errors
                return Response(data)
        elif request.method == "DELETE":
            pk = data["pk"]
            mas = MultipleAnswer.objects.get(pk=pk)
            mas.delete()
            data['success'] = "Multiple Answer Deleted Successfully"
        else:
            data['error'] = "Method is not POST"
            return Response(data)
    else:
        data['error'] = "Not an Institute Login"
        return Response(data)
    return Response(data)


@api_view(["POST", "GET", "PATCH", "DELETE"])
def LongAnswerQuestionAPI(request):
    if request.method == "GET":
        laq = LongAnswerQuestion.objects.all()
        laq = serializers.serialize('json', laq)
        return HttpResponse(laq, content_type="text/json-comment-filtered")
    data = request.data
    examid = data['examid']
    exam = Exam.objects.get(id=examid)
    data['exam'] = exam.pk

    if request.session["type"] == "Institute":
        if request.method == "POST":
            laqs = LongAnswerQuestionSerializer(data=data)
            if laqs.is_valid():
                laqs.save()
                data['success'] = "Long Answer Question Added Successfully!"
            else:
                data['error'] = laqs.errors
                return Response(data)
        elif request.method == "PATCH":
            pk = data['pk']
            laqs = LongAnswerQuestion.objects.get(pk=pk)
            laqs = LongAnswerQuestionSerializer(laqs, data=data, partial=True)
            if laqs.is_valid():
                laqs.save()
                data['success'] = "Long Answer Question Updated Successfully!"
            else:
                data['error'] = laqs.errors
                return Response(data)
        elif request.method == "DELETE":
            pk = data["pk"]
            laqs = LongAnswerQuestion.objects.get(pk=pk)
            laqs.delete()
            data['success'] = "Long Answer Question Deleted Successfully"
        else:
            data['error'] = "Method is not POST"
            return Response(data)
    else:
        data['error'] = "Not an Institute Login"
        return Response(data)
    return Response(data)


@api_view(["POST", "GET", "PATCH", "DELETE"])
def BooleanQuestionAPI(request):
    if request.method == "GET":
        bq = BooleanQuestion.objects.all()
        bq = serializers.serialize('json', bq)
        return HttpResponse(bq, content_type="text/json-comment-filtered")
    data = request.data
    examid = data['examid']
    exam = Exam.objects.get(id=examid)
    data['exam'] = exam.pk

    if request.session["type"] == "Institute":
        if request.method == "POST":
            bqs = BooleanQuestionSerializer(data=data)
            if bqs.is_valid():
                bqs.save()
                data['success'] = "Boolean Question Added Successfully!"
            else:
                data['error'] = bqs.errors
                return Response(data)
        elif request.method == "PATCH":
            pk = data['pk']
            bqs = BooleanQuestion.objects.get(pk=pk)
            bqs = BooleanQuestionSerializer(bqs, data=data, partial=True)
            if bqs.is_valid():
                bqs.save()
                data['success'] = "Boolean Question Updated Successfully!"
            else:
                data['error'] = bqs.errors
                return Response(data)
        elif request.method == "DELETE":
            pk = data["pk"]
            bqs = BooleanQuestion.objects.get(pk=pk)
            bqs.delete()
            data['success'] = "Boolean Question Deleted Successfully"
        else:
            data['error'] = "Method is not POST"
            return Response(data)
    else:
        data['error'] = "Not an Institute Login"
        return Response(data)
    return Response(data)


@api_view(["POST", "GET", "PATCH", "DELETE"])
def ShortAnswerQuestionAPI(request):
    if request.method == "GET":
        saq = ShortAnswerQuestion.objects.all()
        saq = serializers.serialize('json', saq)
        return HttpResponse(saq, content_type="text/json-comment-filtered")
    data = request.data
    examid = data['examid']
    exam = Exam.objects.get(id=examid)
    data['exam'] = exam.pk

    if request.session["type"] == "Institute":
        if request.method == "POST":
            saqs = ShortAnswerQuestionSerializer(data=data)
            if saqs.is_valid():
                saqs.save()
                data['success'] = "Short Answer Question Added Successfully!"
            else:
                data['error'] = saqs.errors
                return Response(data)
        elif request.method == "PATCH":
            pk = data['pk']
            saqs = ShortAnswerQuestion.objects.get(pk=pk)
            saqs = ShortAnswerQuestionSerializer(saqs, data=data, partial=True)
            if saqs.is_valid():
                saqs.save()
                data['success'] = "Short Answer Question Updated Successfully!"
            else:
                data['error'] = saqs.errors
                return Response(data)
        elif request.method == "DELETE":
            pk = data["pk"]
            saqs = ShortAnswerQuestion.objects.get(pk=pk)
            saqs.delete()
            data['success'] = "Short Answer Question Deleted Successfully"
        else:
            data['error'] = "Method is not POST"
            return Response(data)
    else:
        data['error'] = "Not an Institute Login"
        return Response(data)
    return Response(data)


@api_view(["POST", "GET", "PATCH", "DELETE"])
def TutorExamAPI(request):
    if request.method == "GET":
        exam = TutorExam.objects.all()
        exam = serializers.serialize('json', exam)
        return HttpResponse(exam, content_type="text/json-comment-filtered")
    data = request.data
    user = User.objects.get(username=request.user)
    teacher = Teacher.objects.get(user=user)
    data['teacher'] = teacher.pk
    courseid = data['courseID']
    course = Courses.objects.get(courseID=courseid)
    data['course'] = course.pk

    if request.session["type"] == "Teacher":
        if request.method == "POST":
            exam = TutorExamSerializer(data=data)
            if exam.is_valid():
                exam.save()
                data['success'] = "Tutor Exam Added Successfully!"
            else:
                data['error'] = exam.errors
                return Response(data)
        elif request.method == "PATCH":
            pk = data['pk']
            exam = TutorExam.objects.get(pk=pk)
            exam = TutorExamSerializer(exam, data=data, partial=True)
            if exam.is_valid():
                exam.save()
                data['success'] = "Tutor Exam Updated Successfully!"
            else:
                data['error'] = exam.errors
                return Response(data)
        elif request.method == "DELETE":
            pk = data["pk"]
            exam = TutorExam.objects.get(pk=pk)
            exam.delete()
            data['success'] = "Tutor Exam Deleted Successfully"
        else:
            data['error'] = "Method is not POST"
            return Response(data)
    else:
        data['error'] = "Not a Teacher Login"
        return Response(data)
    return Response(data)


@api_view(["POST", "GET", "PATCH", "DELETE"])
def TutorMultipleQuestionAPI(request):
    if request.method == "GET":
        mq = TutorMultipleQuestion.objects.all()
        mq = serializers.serialize('json', mq)
        return HttpResponse(mq, content_type="text/json-comment-filtered")
    data = request.data
    examid = data['examid']
    exam = TutorExam.objects.get(id=examid)
    data['exam'] = exam.pk

    if request.session["type"] == "Teacher":
        if request.method == "POST":
            mqs = TutorMultipleQuestionSerializer(data=data)
            if mqs.is_valid():
                mqs.save()
                data['success'] = "Tutor Multiple Quesiton Added Successfully!"
            else:
                data['error'] = mqs.errors
                return Response(data)
        elif request.method == "PATCH":
            pk = data['pk']
            mqs = TutorMultipleQuestion.objects.get(pk=pk)
            mqs = TutorMultipleQuestionSerializer(mqs, data=data, partial=True)
            if mqs.is_valid():
                mqs.save()
                data['success'] = "Tutor Multiple Question Updated Successfully!"
            else:
                data['error'] = mqs.errors
                return Response(data)
        elif request.method == "DELETE":
            pk = data["pk"]
            mqs = TutorMultipleQuestion.objects.get(pk=pk)
            mqs.delete()
            data['success'] = "Tutor Multiple Question Deleted Successfully"
        else:
            data['error'] = "Method is not POST"
            return Response(data)
    else:
        data['error'] = "Not an Institute Login"
        return Response(data)
    return Response(data)


@api_view(["POST", "GET", "PATCH", "DELETE"])
def TutorMultipleAnswerAPI(request):
    if request.method == "GET":
        ma = TutorMultipleAnswer.objects.all()
        ma = serializers.serialize('json', ma)
        return HttpResponse(ma, content_type="text/json-comment-filtered")
    data = request.data
    questionid = data['questionid']
    question = TutorMultipleQuestion.objects.get(id=questionid)
    data['question'] = question.pk

    if request.session["type"] == "Teacher":
        if request.method == "POST":
            mas = TutorMultipleAnswerSerializer(data=data)
            if mas.is_valid():
                mas.save()
                data['success'] = "Tutor Multiple Answers Added Successfully!"
            else:
                data['error'] = mas.errors
                return Response(data)
        elif request.method == "PATCH":
            pk = data['pk']
            mas = TutorMultipleAnswer.objects.get(pk=pk)
            mas = TutorMultipleAnswerSerializer(mas, data=data, partial=True)
            if mas.is_valid():
                mas.save()
                data['success'] = "Tutor Multiple Answers Updated Successfully!"
            else:
                data['error'] = mas.errors
                return Response(data)
        elif request.method == "DELETE":
            pk = data["pk"]
            mas = TutorMultipleAnswer.objects.get(pk=pk)
            mas.delete()
            data['success'] = "Tutor Multiple Answer Deleted Successfully"
        else:
            data['error'] = "Method is not POST"
            return Response(data)
    else:
        data['error'] = "Not a Teacher Login"
        return Response(data)
    return Response(data)


@api_view(["POST", "GET", "PATCH", "DELETE"])
def TutorLongAnswerQuestionAPI(request):
    if request.method == "GET":
        laq = TutorLongAnswerQuestion.objects.all()
        laq = serializers.serialize('json', laq)
        return HttpResponse(laq, content_type="text/json-comment-filtered")
    data = request.data
    examid = data['examid']
    exam = TutorExam.objects.get(id=examid)
    data['exam'] = exam.pk

    if request.session["type"] == "Teacher":
        if request.method == "POST":
            laqs = TutorLongAnswerQuestionSerializer(data=data)
            if laqs.is_valid():
                laqs.save()
                data['success'] = "Tutor Long Answer Question Added Successfully!"
            else:
                data['error'] = laqs.errors
                return Response(data)
        elif request.method == "PATCH":
            pk = data['pk']
            laqs = TutorLongAnswerQuestion.objects.get(pk=pk)
            laqs = TutorLongAnswerQuestionSerializer(
                laqs, data=data, partial=True)
            if laqs.is_valid():
                laqs.save()
                data['success'] = "Tutor Long Answer Question Updated Successfully!"
            else:
                data['error'] = laqs.errors
                return Response(data)
        elif request.method == "DELETE":
            pk = data["pk"]
            laqs = TutorLongAnswerQuestion.objects.get(pk=pk)
            laqs.delete()
            data['success'] = "Tutor Long Answer Question Deleted Successfully"
        else:
            data['error'] = "Method is not POST"
            return Response(data)
    else:
        data['error'] = "Not a Teacher Login"
        return Response(data)
    return Response(data)


@api_view(["POST", "GET", "PATCH", "DELETE"])
def TutorBooleanQuestionAPI(request):
    if request.method == "GET":
        bq = TutorBooleanQuestion.objects.all()
        bq = serializers.serialize('json', bq)
        return HttpResponse(bq, content_type="text/json-comment-filtered")
    data = request.data
    examid = data['examid']
    exam = TutorExam.objects.get(id=examid)
    data['exam'] = exam.pk

    if request.session["type"] == "Teacher":
        if request.method == "POST":
            bqs = TutorBooleanQuestionSerializer(data=data)
            if bqs.is_valid():
                bqs.save()
                data['success'] = "Tutor Boolean Question Added Successfully!"
            else:
                data['error'] = bqs.errors
                return Response(data)
        elif request.method == "PATCH":
            pk = data['pk']
            bqs = TutorBooleanQuestion.objects.get(pk=pk)
            bqs = TutorBooleanQuestionSerializer(bqs, data=data, partial=True)
            if bqs.is_valid():
                bqs.save()
                data['success'] = "Tutor Boolean Question Updated Successfully!"
            else:
                data['error'] = bqs.errors
                return Response(data)
        elif request.method == "DELETE":
            pk = data["pk"]
            bqs = TutorBooleanQuestion.objects.get(pk=pk)
            bqs.delete()
            data['success'] = "Tutor Boolean Question Deleted Successfully"
        else:
            data['error'] = "Method is not POST"
            return Response(data)
    else:
        data['error'] = "Not a Teacher Login"
        return Response(data)
    return Response(data)


@api_view(["POST", "GET", "PATCH", "DELETE"])
def TutorShortAnswerQuestionAPI(request):
    if request.method == "GET":
        saq = TutorShortAnswerQuestion.objects.all()
        saq = serializers.serialize('json', saq)
        return HttpResponse(saq, content_type="text/json-comment-filtered")
    data = request.data
    examid = data['examid']
    exam = TutorExam.objects.get(id=examid)
    data['exam'] = exam.pk

    if request.session["type"] == "Teacher":
        if request.method == "POST":
            saqs = TutorShortAnswerQuestionSerializer(data=data)
            if saqs.is_valid():
                saqs.save()
                data['success'] = "Tutor Short Answer Question Added Successfully!"
            else:
                data['error'] = saqs.errors
                return Response(data)
        elif request.method == "PATCH":
            pk = data['pk']
            saqs = TutorShortAnswerQuestion.objects.get(pk=pk)
            saqs = TutorShortAnswerQuestionSerializer(
                saqs, data=data, partial=True)
            if saqs.is_valid():
                saqs.save()
                data['success'] = "Tutor Short Answer Question Updated Successfully!"
            else:
                data['error'] = saqs.errors
                return Response(data)
        elif request.method == "DELETE":
            pk = data["pk"]
            saqs = TutorShortAnswerQuestion.objects.get(pk=pk)
            saqs.delete()
            data['success'] = "Tutor Short Answer Question Deleted Successfully"
        else:
            data['error'] = "Method is not POST"
            return Response(data)
    else:
        data['error'] = "Not a Teacher Login"
        return Response(data)
    return Response(data)
