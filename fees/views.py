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
        teach = TeachingType.objects.filter(course__intitute=inst, course__archieved=False)
        courses = Courses.objects.filter(intitute=inst, archieved=False)
        forclass = Courses.objects.filter(intitute=inst).values_list('forclass').distinct()
        
        params = {'courses': courses, 'classes':forclass,'teach':teach}
        if request.method == "POST":
            courseID = request.POST.get('courseName')
                
            course = Courses.objects.get(id = courseID)
            courseName = course.courseName
            
            forclass = request.POST.get('forclass')
            teachType = request.POST.get('teaching')
            duration = request.POST.get('duration')
            discValidity = request.POST.get('discValidity')

            try:
                feeDisc = float(request.POST.get('feeDisc'))
            except:
                feeDisc = 0
            try:
                fee_amt = float(request.POST.get('feeamt'))
                tax = float(request.POST.get('tax'))
                final_amt = float(request.POST.get('final'))
                extraChargeType = int(request.POST.get('chargeType'))
                no_of_installment1 = request.POST.getlist('no_of_installment')
                no_of_installment = ','.join(no_of_installment1)
                no_of_installment1 = [int(x) for x in no_of_installment1]
                extra_charge1 = request.POST.getlist('echarge')
                extra_charge = ','.join(extra_charge1)
                extra_charge1 = [float(x) if x else 0 for x in extra_charge1]
            except Exception as e:
                return HttpResponse(f"Wrong Data Type! - {e}" )
            finalValue = final_amt
            if feeDisc:
                discount = int((finalValue*feeDisc)/100)
                finalValue = finalValue - discount

            if(extraChargeType):
                finalValue = finalValue + sum(extra_charge1)
            else:
                extra_charge1 = [((fee_amt*x)/100) for x in extra_charge1]
                feeCalc = finalValue + sum(extra_charge1)
                
            addFees = AddFeesC(
                    course = course,
                    intitute=inst,
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
                    feeDisc=feeDisc,
                )
            if feeDisc:
                addFees.discValidity = datetime.strptime(discValidity, '%Y-%m-%d')
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
    qry = AddFeesC.objects.get(id=id)

    user = User.objects.get(username=request.session['user'])
    inst = Institute.objects.get(user=user)
    teach = TeachingType.objects.filter(course__intitute=inst, course__archieved=False)
    courses = Courses.objects.filter(intitute=inst, archieved=False)
    forclass = Courses.objects.filter(intitute=inst).values_list('forclass').distinct()

    params = {
        'qry': qry,
        'exch':qry.extra_charge.split(','),
        'courses': courses,
        'classes':forclass,
        'teach':teach
    }
      
    if request.method == "POST":
        courseID = request.POST.get('courseName')
        course = Courses.objects.get(id = courseID)
        courseName = course.courseName
        forclass = request.POST.get('forclass')
        teachType = request.POST.get('teaching')
        duration = request.POST.get('duration')
        discValidity = request.POST.get('discValidity')
        try:
            feeDisc = float(request.POST.get('feeDisc'))
        except:
            feeDisc = 0
        try:
            fee_amt = float(request.POST.get('feeamt'))
            tax = float(request.POST.get('tax'))
            final_amt = float(request.POST.get('final'))
            extraChargeType = int(request.POST.get('chargeType'))
            no_of_installment1 = request.POST.getlist('no_of_installment')
            no_of_installment = ','.join(no_of_installment1)
            no_of_installment1 = [int(x) for x in no_of_installment1]
            extra_charge1 = request.POST.getlist('echarge')
            extra_charge = ','.join(extra_charge1)
            extra_charge1 = [float(x) if x else 0 for x in extra_charge1]
        except Exception as e:
            return HttpResponse(f"Wrong Data Type! - {e}")
        finalValue = final_amt
        if feeDisc:
            discount = int((finalValue*feeDisc)/100)
            finalValue = finalValue - discount

        if(extraChargeType):
            finalValue = finalValue + sum(extra_charge1)
        else:
            extra_charge1 = [((fee_amt*x)/100) for x in extra_charge1]
            feeCalc = finalValue + sum(extra_charge1)
            
        addf = AddFeesC.objects.filter(id=id).update(
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
            feeDisc=feeDisc,
        )

        for i in AddFeesC.objects.filter(id=id):
            if feeDisc:
                i.discValidity = datetime.strptime(discValidity, '%Y-%m-%d')
            else:
                i.discValidity = None

        return redirect("viewFees")
    return render(request, 'fees/editFee.html', context=params)

@login_required(login_url='Login')
def submitFee(request):
    if request.session["type"] == "Institute":
        user = User.objects.get(username=request.session['user'])
        inst = Institute.objects.get(user=user)
        
        stud = AddStudentInst.objects.filter(institute = inst)
        addstud=[]
        addstufirst =[]
        
        for i in stud:
            stu = i.student.user.username
            addstud.append(stu)
            stufirst = i.student.user.first_name
            addstufirst.append(stufirst)    
        

        submitfees = SubmitFees.objects.filter( student__user__first_name__in = addstufirst)
        addfeescourse = AddFeesC.objects.filter(intitute = inst )
        mydataf = zip(stud, submitfees)
        ctx ={'stud':stud,'submitfees':submitfees,'addfeescourse':addfeescourse,'mydataf':mydataf}

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
                feeslist = []
                userId = request.POST.get('userId')
                user = AddStudentInst.objects.get(id=userId)
                
                student = user.student
                student = AddStudentInst.objects.filter(
                    Q(student__user__username=student) & Q(institute=inst))
                
                for stu in student:                 
                    course = stu.courseName                       
                    fee = AddFeesC.objects.filter(Q(courseName=course) & Q(forclass=stu.forclass)).first()
                    totalfees = float(fee.final_amount)
                    print(fee)     
                    feeslist.append(totalfees) 

                mydata = zip(student, feeslist)
                return render(request, 'fees/submitFee.html', {'mydata': mydata, "user": user})

            elif(userAction == 'studentFee'):
                subjectId = request.POST.get('subjectId')
                dataObj = AddStudentInst.objects.get(id=subjectId)
                finalfees = request.POST.get("studentfinalfee",None)

                addfess = AddFeesC.objects.all()
                addFeeObj = AddFeesC.objects.filter(Q(courseName = dataObj.courseName) & Q(forclass = dataObj.forclass))     
                if(addFeeObj):
                    addFeeObj = addFeeObj[0]
                else:
                    return HttpResponse(f"Fees for this subject Combination doesnot Exist! <br>courseName  = {dataObj.courseName},<br>forclass = {dataObj.forclass},<br>teachType = {dataObj.teachType}")
                
                if SubmitFees.objects.filter(student = dataObj.student,fees = addFeeObj):
                    feeObj =  SubmitFees.objects.filter(student = dataObj.student,fees = addFeeObj)[0]

                else:
                    feeObj = SubmitFees(
                        student = dataObj.student,
                        fees = addFeeObj,
                        totalFee = addFeeObj.final_amount,
                        feePayed = 0,
                        instalmentDue = addFeeObj.no_of_installment,
                        totalInstallments = addFeeObj.no_of_installment)                   
                    feeObj.save()

                feeamt = float(addFeeObj.fee_amt)
                disc = float(addFeeObj.feeDisc)
                tax = float(addFeeObj.tax)
                no_of_i = int(addFeeObj.no_of_installment)
                disc_fee = feeamt + float((feeamt*(tax-disc)/100))
                i = int(feeObj.totalInstallments) - int(feeObj.instalmentDue) - 1
                expected = disc_fee/no_of_i
                if i>-1 and i < no_of_i-2:
                    if(addFeeObj.typeOfCharge):
                        expected += int(addFeeObj.extra_charge.split(',')[i])
                    else:
                        expected += expected * int(addFeeObj.extra_charge.split(',')[i])/100
                if i == no_of_i-2:
                    expected = feeObj.totalFee - feeObj.feePayed

                inputData = {
                    'installmentNumber': int(feeObj.totalInstallments) - int(feeObj.instalmentDue) + 1,
                    'feeId': feeObj.id,
                }
                installmentnotcomplete = (feeObj.instalmentDue != 0)
                return render(
                    request,
                    'fees/submitFee.html',
                    {
                        'installmentsDone':Instalment.objects.filter(feeObj=feeObj), 'inputData': inputData, 'feeObj': feeObj, 'expected':expected, 'installmentnotcomplete': installmentnotcomplete,'dataObj':dataObj,'finalfees':feeObj.totalFee
                    }
                )
            elif(userAction == 'submitFee'):
                iNum = int(float(request.POST.get('iNum')))
                fees = int(float(request.POST.get('fees')))
                payed = int(float(request.POST.get('payed')))
                
                feeId = request.POST.get('feeId')

                submitObj = SubmitFees.objects.get(id = feeId)
                submitObj.feePayed = submitObj.feePayed + payed
                submitObj.instalmentDue = submitObj.instalmentDue - 1
                submitObj.save()
                newInstallment = Instalment(
                    feeObj=submitObj,
                    instalmentNum=iNum,
                    paymentExp=fees,
                    paymentDone=payed
                )
                newInstallment.save()
        return render(request, 'fees/submitFee.html',ctx)
    return messages.error(request, "You Are not Authenticated User for this Page")

@login_required(login_url='Login')
def archiveFeefirst(request,id):
    if request.session['type']=='Institute':
        user = User.objects.get(username=request.session['user'])
        inst = Institute.objects.get(user=user)         
        fees = AddFeesC.objects.get(id=id)
        fees.archieved = True
        fees.save()
        messages.warning(request, "Fees Added to Archive Successfully")
        return redirect("archiveFeeList")
    return HttpResponse("You Are Not Authenticated for this Page")


@login_required(login_url='Login')
def unarchiveFee(request,id):
    if request.session['type']=='Institute':
        user = User.objects.get(username=request.session['user'])
        inst = Institute.objects.get(user=user)         
        fees = AddFeesC.objects.get(id=id)
        fees.archieved = False
        fees.save()
        messages.success(request, "Fees Removed from Archive Successfully")
        return redirect("archiveFeeList")
    return HttpResponse("You Are Not Authenticated for this Page")



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
