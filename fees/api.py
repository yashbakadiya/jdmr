from django.shortcuts import render, redirect, HttpResponse
from .models import AddFeesC, SubmitFees, Instalment
from courses.models import Courses, TeachingType
from accounts.models import Institute, Teacher, Student
from django.contrib.auth.models import User
import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from .serializers import AddFeesSerializer, SubmitFeesSerializer, NewInstallmentSerializer
from django.core import serializers
from django.db.models import Q
from datetime import datetime, timedelta


@api_view(["POST", "GET", "PATCH", "DELETE"])
def AddFeesAPI(request):
    data = request.data
    if request.session["type"] == "Institute":
        username = data['username']
        user = User.objects.get(username=username)
        inst = Institute.objects.get(user=user)
        if request.method == "GET":
            courses = Courses.objects.filter(intitute=inst)
            if data['archive'] == True:
                archive = list(data['archive'].split(','))
                for x in archive:
                    arTutor = AddFeesC.objects.get(id=int(x))
                    arTutor.archieved = True
                    arTutor.save()
                data['success'] = "Fees Added to Archieve Successfully"
                return Response(data)
            fees = []
            try:
                for course in courses:
                    if AddFeesC.objects.filter(course=course, archieved=False).exists():
                        fees.extend(AddFeesC.objects.filter(
                            course=course, archieved=False))
            except:
                fees = []
            data['fees'] = fees
            data['centre'] = inst.pk
            return Response(data)

        data['intitute'] = inst.pk
        course = TeachingType.objects.filter(
            course__intitute=inst, course__archieved=False)
        courses = []
        for c in course:
            cou = Courses.objects.get(id=c.courseID)
            courses.append(cou)
        #data['courses'] = courses
        if request.method == "POST":
            forclass = data['forclass']
            teachType = data['teachType']
            if 'ajax_getinfo' in data:
                courseID = data['courseID']
                qry = TeachingType.objects.filter(
                    Q(courseID__icontains=courseID))
                a = TeachingType.objects.filter(Q(courseID__icontains=courseID)).values(
                    'forclass', 'teachType', 'duration')
                b = list(a)
                c = b[0]["forclass"]
                t = b[0]["teachType"]
                d = b[0]["duration"]
                data['classes'] = list(c.split(', '))
                data['teachings'] = list(t.split('\n'))
                data['durations'] = list(d.split('\n'))
                return Response(data)
            else:
                courseID = data['courseID']
                course = Courses.objects.filter(id=courseID, intitute=inst)[0]
                data['course'] = course.pk
                forclass = data['forclass']
                teachType = data['teachType']
                duration = data['duration']
                discValidity = data['discValidity']
                data['discValidity'] = datetime.strptime(
                    discValidity, '%Y-%m-%d')
            try:
                data['feeDisc'] = float(data['feeDisc'])
                data['fee_amt'] = float(data['fee_amt'])
                data['tax'] = float(data['tax'])
                data['final_amt'] = float(data['final_amt'])
                data['typeOfCharge'] = int(data['typeOfCharge'])
                no_of_installment1 = data['no_of_installment']
                data['no_of_installment'] = ','.join(no_of_installment1)
                no_of_installment1 = [int(x) for x in no_of_installment1]
                extra_charge1 = data['extra_charge']
                data['extra_charge'] = ','.join(extra_charge1)
                extra_charge1 = [float(x) for x in extra_charge1]
            except Exception as e:
                data['error'] = f"Wrong Data Type! - {e}"
                return Response(data)
            finalValue = 0
            if(data['typeOfCharge']):
                finalValue = data['final_amt'] + sum(extra_charge1)
            else:
                extra_charge1 = [((data['fee_amt']*x)/100)
                                 for x in extra_charge1]
                feeCalc = data['fee_amt'] + sum(extra_charge1)
                finalValue = feeCalc + ((feeCalc*data['tax'])/100)
            finalValue -= data['feeDisc']
            data['final_amount'] = finalValue
            afs = AddFeesSerializer(data=data)
            if afs.is_valid():
                afs.save()
                data['success'] = "Fees Added Successfully"
            else:
                data['error'] = afs.errors
                return Response(data)
        elif request.method == "PUT":
            forclass = data['forclass']
            teachType = data['teachType']
            if 'ajax_getinfo' in data:
                courseID = data['courseID']
                qry = TeachingType.objects.filter(
                    Q(courseID__icontains=courseID))
                a = TeachingType.objects.filter(Q(courseID__icontains=courseID)).values(
                    'forclass', 'teachType', 'duration')
                b = list(a)
                c = b[0]["forclass"]
                t = b[0]["teachType"]
                d = b[0]["duration"]
                data['classes'] = list(c.split(', '))
                data['teachings'] = list(t.split('\n'))
                data['durations'] = list(d.split('\n'))
                return Response(data)
            else:
                courseID = data['courseID']
                course = Courses.objects.filter(id=courseID, intitute=inst)[0]
                data['course'] = course.pk
                forclass = data['forclass']
                teachType = data['teachType']
                duration = data['duration']
                discValidity = data['discValidity']
                data['discValidity'] = datetime.strptime(
                    discValidity, '%Y-%m-%d')
            try:
                data['feeDisc'] = float(data['feeDisc'])
                data['fee_amt'] = float(data['fee_amt'])
                data['tax'] = float(data['tax'])
                data['final_amt'] = float(data['final_amt'])
                data['typeOfCharge'] = int(data['typeOfCharge'])
                no_of_installment1 = data['no_of_installment']
                data['no_of_installment'] = ','.join(no_of_installment1)
                no_of_installment1 = [int(x) for x in no_of_installment1]
                extra_charge1 = data['extra_charge']
                data['extra_charge'] = ','.join(extra_charge1)
                extra_charge1 = [float(x) for x in extra_charge1]
            except Exception as e:
                data['error'] = f"Wrong Data Type! - {e}"
                return Response(data)
            finalValue = 0
            if(data['typeOfCharge']):
                finalValue = data['final_amt'] + sum(extra_charge1)
            else:
                extra_charge1 = [((data['fee_amt']*x)/100)
                                 for x in extra_charge1]
                feeCalc = data['fee_amt'] + sum(extra_charge1)
                finalValue = feeCalc + ((feeCalc*data['tax'])/100)
            finalValue -= data['feeDisc']
            data['final_amount'] = finalValue
            addfees = AddFeesC.objects.get(pk=data['pk'])
            afs = AddFeesSerializer(addfees, data=data)
            if afs.is_valid():
                afs.save()
                data['success'] = "Fees Updated Successfully"
            else:
                data['error'] = afs.errors
                return Response(data)
        elif request.method == "DELETE":
            pk = data["pk"]
            afs = AddFeesC.objects.get(pk=pk)
            afs.delete()
            data['success'] = "Fees Deleted Successfully"
        else:
            data['error'] = "Method is not POST"
            return Response(data)
    else:
        data['error'] = "Not an Institute Login"
        return Response(data)
    return Response(data)

# studentsearch and subjectsearch is incomplete
# require some models from student app


@api_view(["POST", "GET", "PATCH", "DELETE"])
def SubmitFeesAPI(request):
    data = request.data
    if request.session["type"] == "Institute":
        if request.method == 'POST':
            user = User.objects.get(username=request.session['user'])
            inst = Institute.objects.get(user=user)
            userAction = data["userAction"]
            if(userAction == 'studentSearch'):
                name = data["userName"]
                data = AddStudentInst.objects.filter((
                    Q(student__user__username__contains=name) |
                    Q(student__user__first_name__contains=name) |
                    Q(student__user__last_name__contains=name) |
                    Q(student__user__email__contains=name)) &
                    Q(institute=inst),
                )
                return render(request, 'fees/submitFee.html', {'userData': data})
            elif(userAction == 'subjectSearch'):
                print(request.POST)
                feeslist = []
                userId = request.POST.get('userId')
                user = AddStudentInst.objects.get(id=userId)
                student = user.student
                student = AddStudentInst.objects.filter(
                    Q(student__user__username=student) & Q(institute=inst))
                print('student--', student)
                for stu in student:
                    print("stu--", stu.student)
                    course = stu.courseName
                    print("course--", course)
                    fee = AddFeesC.objects.filter(
                        Q(courseName=course) & Q(intitute=inst)).first()
                    print('fees--', fee)
                    fee = (fee.final_amount-(fee.final_amount/100)*stu.feeDisc)
                    print('fee--', fee)
                    feeslist.append(fee)
                print("feeslist--", feeslist)
                mydata = zip(student, feeslist)
                return render(request, 'fees/submitFee.html', {'mydata': mydata, "user": user})

            elif(userAction == 'studentFee'):
                subjectId = data['subjectId']
                studentobj = Student.objects.get(id=subjectId)
                print(studentobj.instalment)
                addFeeObj = AddFeesC.objects.filter(
                    courseName=studentobj.courseName,
                    forclass=studentobj.forclass,
                    teachType=studentobj.teachType
                )
                print(addFeeObj)
                if(addFeeObj):
                    addFeeObj = addFeeObj[0]
                else:
                    return HttpResponse(f"Fees for this subject Combination doesnot Exist! <br>courseName  = {studentobj.courseName},<br>forclass = {studentobj.forclass},<br>teachType = {studentobj.teachType}")
                feeObj = studentobj.fees.all()
                print(feeObj)
                if(not feeObj):
                    data['student'] = studentobj
                    data['subject'] = addFeeObj.courseName
                    data['totalFee'] = addFeeObj.final_amount
                    data['balanceFee'] = addFeeObj.final_amount
                    data['totalInstallments'] = studentobj.instalment
                    data['instalmentDue'] = studentobj.instalment
                    feeserializer = SubmitFeesSerializer(data=data)
                    if feeserializer.is_valid():
                        feeserializer.save()
                        data['success'] = "Student Fee added Succesfully"
                    feeObj = studentobj.fees.all()

                feeObj = feeObj[0]
                print(feeObj.instalmentDue)
                try:
                    payment = feeObj.balanceFee/feeObj.instalmentDue
                except:
                    payment = feeObj.balanceFee
                print(payment)
                inputData = {
                    'installmentNumber': feeObj.totalInstallments - feeObj.instalmentDue + 1,
                    'payment': payment,
                    'feeId': feeObj.sno,
                }
                data['inputData'] = inputData
                installmentnotcomplete = (feeObj.instalmentDue != 0)
                data['installmentsDone'] = feeObj.totalInstallments - \
                    feeObj.instalmentDue
                data['feeObj'] = feeObj,
                data['installmentnotcomplete'] = installmentnotcomplete
                return Response(data)
            elif(userAction == 'submitFee'):
                iNum = int(float(data['iNum']))
                fees = float(data['fees'])
                payed = float(data['payed'])
                feeId = int(float(data['feeId']))
                submitObj = SubmitFees.objects.get(sno=feeId)
                submitObj.feePayed = F('feePayed') + payed
                submitObj.balanceFee = F('balanceFee') - payed
                submitObj.instalmentDue = F('instalmentDue') - 1
                submitObj.save()
                data['feeObj'] = submitObj
                data['instalmentNum'] = iNum
                data['paymentExp'] = fees
                data['paymentDone'] = payed
                newInstallment = NewInstallmentSerializer(data=data)
                if newInstallment.is_valid():
                    newInstallment.save()
                    data['success2'] = 'Installment saved'
                    return Response(data)
                else:
                    data['error'] = newInstallment.errors
                    return Response(data)
    data['error'] = "User not Authenticated"
    return Response(data)
