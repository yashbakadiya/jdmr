from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from courses.models import Courses, TeachingType
from accounts.models import Institute, Teacher, Student
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.db.models import Q
from datetime import datetime, timedelta
from django.forms.models import model_to_dict
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.models import User
from students.models import AddStudentInst
# Create your views here.


@login_required(login_url='Login')
def addFeesC(request):
    if request.session['type'] == 'Institute':
        user = User.objects.get(username=request.session['user'])
        inst = Institute.objects.get(user=user)
        course = TeachingType.objects.filter(course__intitute=inst, course__archieved=False)
        print('couseteaching',course)
        forclas=Courses.objects.all()
        print('forclass',forclas)
        
        courses = []
        print('course_teaching',course)

        for c in course:
            cou = Courses.objects.get(id=c.courseID)
            courses.append(cou)
            
        print('courses',courses)
        params = {'courses': courses, 'forclas':forclas}
        if request.method == "POST":
            forclass = request.POST.get('forclas')
            teachType = request.POST.get('teachType')
            if 'ajax_getinfo' in request.POST:
                courseID = request.POST.get('courseID')
                qry = TeachingType.objects.filter(Q(courseID__icontains=courseID))
                a = TeachingType.objects.filter(Q(courseID__icontains=courseID)).values('forclass', 'teachType', 'duration')
                b = list(a)
                c = b[0]["forclass"]
                t = b[0]["teachType"]
                d = b[0]["duration"]
                classes = list(c.split(', '))
                teachings = list(t.split('\n'))
                durations = list(d.split('\n'))
                param = {'classes': classes,
                         'teachings': teachings, 'durations': durations}
                return JsonResponse(param)
            else:
                courseID = request.POST.get('courseID')
                course = Courses.objects.filter(id=courseID, intitute=inst)[0]
                forclass = request.POST.get('forclas')
                teachType = request.POST.get('check')
                duration = request.POST.get('duration')
                discValidity = request.POST.get('discValidity')
                discValidity = datetime.strptime(discValidity, '%Y-%m-%d')

                try:
                    feeDisc = float(request.POST.get('feeDisc'))
                    fee_amt = float(request.POST.get('feeamt'))
                    tax = float(request.POST.get('tax'))
                    final_amt = float(request.POST.get('final'))
                    extraChargeType = int(request.POST.get('chargeType'))
                    no_of_installment1 = request.POST.getlist(
                        'no_of_installment')
                    no_of_installment = ','.join(no_of_installment1)
                    no_of_installment1 = [int(x) for x in no_of_installment1]
                    extra_charge1 = request.POST.getlist('echarge')
                    extra_charge = ','.join(extra_charge1)
                    extra_charge1 = [float(x) for x in extra_charge1]
                except Exception as e:
                    return HttpResponse(f"Wrong Data Type! - {e}")
                finalValue = 0
                if(extraChargeType):
                    finalValue = final_amt + sum(extra_charge1)
                else:
                    extra_charge1 = [((fee_amt*x)/100) for x in extra_charge1]
                    feeCalc = fee_amt + sum(extra_charge1)
                    finalValue = feeCalc + ((feeCalc*tax)/100)
                finalValue -= feeDisc
                addFees = AddFeesC(
                    course=course,
                    intitute=inst,
                    courseName=courseID,
                    forclass=forclass,
                    teachType=teachType,
                    duration=duration,
                    fee_amt=fee_amt,
                    tax=tax,
                    final_amt=final_amt,
                    no_of_installment=no_of_installment,
                    extra_charge=extra_charge,
                    typeOfCharge=extraChargeType,
                    final_amount=finalValue,
                    discValidity=discValidity,
                    feeDisc=feeDisc,
                )
                addFees.save()
                messages.success(request, "Fees Added Successfully")
                return redirect("viewFees")
        return render(request, 'fees/addFees.html', params)
    return messages.error(request, "You Are not Authenticated User for this Page")


@login_required(login_url='Login')
def viewFees(request):
    if request.session['type'] == "Institute":
        user = User.objects.get(username=request.session['user'])
        inst = Institute.objects.get(user=user)
        courses = Courses.objects.filter(intitute=inst)
        if request.method == "POST":
            check = request.POST.getlist('check')
            for x in check:
                arTutor = AddFeesC.objects.get(id=int(x))
                arTutor.archieved = True
                arTutor.save()
                messages.warning(
                    request, "Fees Added to Archieve Successfully")
                return redirect("viewFees")
        fees = []
        try:
            for course in courses:
                if AddFeesC.objects.filter(course=course, archieved=False).exists():
                    fees.extend(AddFeesC.objects.filter(
                        course=course, archieved=False))
        except:
            fees = []
        params = {'fees': fees, 'centre': inst}
        return render(request, 'fees/viewFees.html', params)
    return messages.error(request, "You Are not Authenticated User for this Page")


@login_required(login_url="Login")
def deleteFee(request, id):
    if request.session['type'] == "Institute":
        delfee = AddFeesC.objects.get(id=id)
        delfee.delete()
        messages.warning(request, "Fees Deleted Successfully")
        return redirect("viewFees")
    return HttpResponse("You not Authenticated for this Page")


@login_required(login_url="Login")
def editFee(request, id):
    params = {}
    qry = AddFeesC.objects.get(id=id)
    params['qry'] = qry
    params['jsonqry'] = model_to_dict(qry)
    params['jsonqry'] = json.dumps(params['jsonqry'], cls=DjangoJSONEncoder)
    courses = TeachingType.objects.all()
    params['courses'] = courses
    if request.method == "POST":
        if 'ajax_getinfo' in request.POST:
            courseName = request.POST.get('courseName')
            qry = TeachingType.objects.filter(
                Q(courseName__icontains=courseName))
            a = TeachingType.objects.filter(Q(courseName__icontains=courseName)).values(
                'forclass', 'teachType', 'duration')
            b = list(a)
            c = b[0]["forclass"]
            t = b[0]["teachType"]
            d = b[0]["duration"]
            classes = list(c.split(', '))
            teachings = list(t.split('\n'))
            durations = list(d.split('\n'))
            param = {'classes': classes,
                     'teachings': teachings, 'durations': durations}
            return JsonResponse(param)
        else:
            courseName = request.POST.get('courseName')
            forclass = request.POST.get('forclass')
            teachType = request.POST.get('check')
            duration = request.POST.get('duration')
            discValidity = request.POST.get('validity')
            discValidity = datetime.strptime(discValidity, '%Y-%m-%d')
            try:
                feeDisc = float(request.POST.get('discount'))
                fee_amt = float(request.POST.get('feeamt'))
                tax = float(request.POST.get('tax'))
                final_amt = float(request.POST.get('final'))
                extraChargeType = int(request.POST.get('chargeType'))
                no_of_installment1 = request.POST.getlist('no_of_installment')
                no_of_installment = ','.join(no_of_installment1)
                no_of_installment1 = [int(x) for x in no_of_installment1]
                extra_charge1 = request.POST.getlist('echarge')
                extra_charge = ','.join(extra_charge1)
                extra_charge1 = [float(x) for x in extra_charge1]
            except Exception as e:
                return HttpResponse(f"Wrong Data Type! - {e}")
            finalValue = 0
            if(extraChargeType):
                finalValue = final_amt + sum(extra_charge1)
            else:
                extra_charge1 = [((fee_amt*x)/100) for x in extra_charge1]
                feeCalc = fee_amt + sum(extra_charge1)
                finalValue = feeCalc + ((feeCalc*tax)/100)
            finalValue -= feeDisc
            AddFeesC.objects.filter(id=id).update(
                courseName=courseName,
                forclass=forclass,
                teachType=teachType,
                duration=duration,
                fee_amt=fee_amt,
                tax=tax,
                final_amt=final_amt,
                no_of_installment=no_of_installment,
                extra_charge=extra_charge,
                typeOfCharge=extraChargeType,
                final_amount=finalValue,
                discValidity=discValidity,
                feeDisc=feeDisc,
            )
            return redirect("viewFees")
    return render(request, 'fees/editFee.html', params)


@login_required(login_url='Login')
def submitFee(request):
    if request.session["type"] == "Institute":
        if request.method == 'POST':
            user = User.objects.get(username=request.session['user'])
            inst = Institute.objects.get(user=user)
            userAction = request.POST.get("userAction", None)
            if(userAction == 'studentSearch'):
                name = request.POST.get("userName")
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
                subjectId = request.POST.get('subjectId')
                dataObj = Student.objects.get(id=subjectId)
                print(dataObj.instalment)
                addFeeObj = AddFeesC.objects.filter(
                    courseName=dataObj.courseName,
                    forclass=dataObj.forclass,
                    teachType=dataObj.teachType
                )
                print(addFeeObj)
                if(addFeeObj):
                    addFeeObj = addFeeObj[0]
                else:
                    return HttpResponse(f"Fees for this subject Combination doesnot Exist! <br>courseName  = {dataObj.courseName},<br>forclass = {dataObj.forclass},<br>teachType = {dataObj.teachType}")
                feeObj = dataObj.fees.all()
                print(feeObj)
                if(not feeObj):
                    feeObjNew = SubmitFees(
                        username=dataObj,
                        subject=addFeeObj.courseName,
                        totalFee=addFeeObj.final_amount,
                        balanceFee=addFeeObj.final_amount,
                        totalInstallments=dataObj.instalment,
                        instalmentDue=dataObj.instalment
                    )
                    print("bs", feeObjNew.instalmentDue)
                    feeObjNew.save()
                    feeObj = dataObj.fees.all()

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
                installmentnotcomplete = (feeObj.instalmentDue != 0)
                return render(
                    request,
                    'fees/submitFee.html',
                    {
                        'inputData': inputData, 'installmentsDone': feeObj.totalInstallments - feeObj.instalmentDue, 'feeObj': feeObj, 'installmentnotcomplete': installmentnotcomplete
                    }
                )
            elif(userAction == 'submitFee'):
                iNum = int(float(request.POST.get('iNum')))
                fees = float(request.POST.get('fees'))
                payed = float(request.POST.get('payed'))
                feeId = int(float(request.POST.get('feeId')))
                submitObj = SubmitFees.objects.get(sno=feeId)
                print(dir(submitObj.feePayed))
                print(submitObj.feePayed.to_integral_value())
                submitObj.feePayed = F('feePayed') + payed
                submitObj.balanceFee = F('balanceFee') - payed
                submitObj.instalmentDue = F('instalmentDue') - 1
                submitObj.save()
                newInstallment = Instalment(
                    feeObj=submitObj,
                    instalmentNum=iNum,
                    paymentExp=fees,
                    paymentDone=payed
                )
                newInstallment.save()
        return render(request, 'fees/submitFee.html')
    return messages.error(request, "You Are not Authenticated User for this Page")


@login_required(login_url='Login')
def archiveFeeList(request):
    if request.session['type'] == "Institute":
        user = User.objects.get(username=request.session['user'])
        inst = Institute.objects.get(user=user)
        if request.method == "POST":
            check = request.POST.getlist('check')
            for x in check:
                arTutor = AddFeesC.objects.get(id=int(x))
                arTutor.archieved = False
                arTutor.save()
                messages.warning(
                    request, "Fees Removed From Archieve Successfully")
                return redirect("archiveFeeList")
        fees = AddFeesC.objects.filter(intitute=inst, archieved=True)
        params = {'fees': fees}
        return render(request, 'fees/archiveFeeList.html', params)
    return messages.error(request, "You Are not Authenticated User for this Page")


@login_required(login_url="Login")
def Studentpayments(request, id):
    if request.session['type'] == "Institute":
        pass
