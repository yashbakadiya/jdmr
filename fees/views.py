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
        print('couser',courses)
        
        
        # courses = []
        # print('course_teaching',course)

        # for c in course:
        #     cou = Courses.objects.get(id=c.courseID)
        #     courses.append(cou)
            
        
        params = {'courses': courses, 'classes':forclass,'teach':teach}
        if request.method == "POST":
            forclass = request.POST.get('forclass')
            print('forclas',forclass)
            teachType = request.POST.get('teaching')
            print('teachingType',teachType)
            if 'ajax_getinfo' in request.POST:
                courseID = request.POST.get('courseName')
                print('courseID',courseID)
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
                courseID = request.POST.get('courseName')
                print('courseID',courseID)

                
                course = Courses.objects.get(id = courseID)
                courseName = course.courseName
                

                forclass = request.POST.get('forclass')
                teachType = request.POST.get('teaching')
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
                    return HttpResponse(f"Wrong Data Type! - {e}" )
                finalValue = 0
                if(extraChargeType):
                    finalValue = final_amt + sum(extra_charge1)
                else:
                    extra_charge1 = [((fee_amt*x)/100) for x in extra_charge1]
                    feeCalc = fee_amt + sum(extra_charge1)
                    finalValue = feeCalc + ((feeCalc*tax)/100)
                
                try:
                    discount = int(finalValue/feeDisc)
                except Exception as e:
                    return HttpResponse(f"Wrong Data Type! - {e}")


                
                    
                finalValue = finalValue - discount
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
 
    


    user = User.objects.get(username=request.session['user'])
    inst = Institute.objects.get(user=user)
    teach = TeachingType.objects.filter(course__intitute=inst, course__archieved=False)
    courses = Courses.objects.filter(intitute=inst, archieved=False)
    forclass = Courses.objects.filter(intitute=inst).values_list('forclass').distinct()
      
        
    params = {'courses': courses, 'classes':forclass,'teach':teach}
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
                extra_charge = request.POST.getlist('echarge')
                # extra_charge = ','.join(extra_charge1)
                # extra_charge1 = [float(x) for x in extra_charge1]
            except Exception as e:
                return HttpResponse(f"Wrong Data Type! - {e}")
            finalValue = 0

            a = final_amt
            print("final_aamt",a)
            b = a - int(a/feeDisc)  
            print("after discount", b)  
            c =b + int(extra_charge) 
            print("after extra chage",c)
            finalValue = c
            # if(extraChargeType):
            #     finalValue = final_amt + int(extra_charge)
            # else:
            #     extra_charge1 = [((fee_amt*x)/100) for x in extra_charge]
            #     feeCalc = fee_amt + sum(extra_charge1)
            #     finalValue = feeCalc + ((feeCalc*tax)/100)
            
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

@login_required(login_url="Login")
def editFeef(request, id):
    params = {}
    qry = AddFeesC.objects.get(id=id)
    user = User.objects.get(username=request.session['user'])
    inst = Institute.objects.get(user=user)
    teach = TeachingType.objects.filter(course__intitute=inst, course__archieved=False)
    courses = Courses.objects.filter(intitute=inst, archieved=False)
    forclass = Courses.objects.filter(intitute=inst).values_list('forclass').distinct()
      
        
    params = {'courses': courses, 'classes':forclass,'teach':teach,'qry':qry}
    if request.method == "POST":
        courseName = request.POST.get('courseName')
        forclass = request.POST.get('forclass')
        teachType = request.POST.get('teaching')
        duration = request.POST.get('duration')        
        fee_amt = int(request.POST.get('feeamt'))
        tax = int(request.POST.get('tax'))
        final_amt = request.POST.get('final')
        
        no_of_installment1 = request.POST.getlist('no_of_installment')
        no_of_installment = ','.join(no_of_installment1)
        extraChargeType = int(request.POST.get('chargeType'))
        feeDisc = request.POST.get('feeDisc')
        discValidity = request.POST.get('discValidity')
        discValidity = datetime.strptime(discValidity, '%Y-%m-%d')


        # discValidity = request.POST.get('discValidity')
        # discValidity = datetime.strptime(discValidity, '%Y-%m-%d')

        
        extra_charge1 = request.POST.getlist('echarge') 
        extra_charge = ','.join(extra_charge1)


        a = final_amt
        print("final_aamt",a)
        b = a - int(a/feeDisc)  
        print("after discount", b)  
        c =b + int(extra_charge) 
        print("after extra chage",c)
        finalValue = c
        # if(extraChargeType):
        #     finalValue = final_amt 
        # else:
        #     extra_charge1 =((fee_amt*x)/100) 
        #     feeCalc = fee_amt + sum(extra_charge1)
        #     finalValue = feeCalc + ((feeCalc*tax)/100)
        #     afterfeesdic = finalValue
        #     finalValue -= feeDisc

        
        qry.courseName = courseName
        qry.forclass = forclass
        qry.teachType = teachType
        qry.duration = duration
        qry.fee_amt = fee_amt
        qry.tax = tax
        qry.final_amt = final_amt
        qry.no_of_installment = no_of_installment
        qry.typeOfCharge = extraChargeType
        qry.extra_charge = extra_charge
        qry.feeDisc = feeDisc
        qry.discValidity = discValidity
        qry.final_amount = finalValue
        qry.archieved = 'False'

        qry.save()
        # AddFeesC.objects.filter(id=id).update(
        #         courseName=courseName,
        #         forclass=forclass,
        #         teachType=teachType,
        #         duration=duration,
        #         fee_amt=fee_amt,
        #         tax=tax,
        #         final_amt=final_amt,
        #         no_of_installment=no_of_installment,
        #         extra_charge=extra_charge,
        #         typeOfCharge=extraChargeType,
        #         final_amount=finalValue,
        #         discValidity=discValidity,
        #         feeDisc=feeDisc, )
        return redirect("viewFees")
    return render(request, 'fees/editFee.html', params)

@login_required(login_url='Login')
def submitFee(request):
    if request.session["type"] == "Institute":
        user = User.objects.get(username=request.session['user'])
        inst = Institute.objects.get(user=user)
        

        stud = AddStudentInst.objects.filter(institute = inst)
        addstud=[]
        addstufirst =[]
        
        for i in stud:
            print(i.institute)
            print(i.courseName)
            stu = i.student.user.username
            addstud.append(stu)
            stufirst = i.student.user.first_name
            addstufirst.append(stufirst)
            

        print('addstu',addstud)   
        print('addstufirst',addstufirst)       
        
        

        submitfees = SubmitFees.objects.filter( student__user__first_name__in = addstufirst)
        print('submitfees',submitfees)      
        addfeescourse = AddFeesC.objects.filter(intitute = inst )
        print('addfeescourse',addfeescourse)
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
                print(request.POST)
                feeslist = []
                userId = request.POST.get('userId')
                user = AddStudentInst.objects.get(id=userId)
                
                print('user',user)
                student = user.student
                print('student subjectSearch',student)
                student = AddStudentInst.objects.filter(
                    Q(student__user__username=student) & Q(institute=inst))
                print('student--', student)
                
                for stu in student:                    
                    print("stu--", stu.student)
                    course = stu.courseName                    
                    print("course--", course)                    
                    fee = AddFeesC.objects.filter(Q(courseName=course) & Q(intitute=inst)).first()
                    print('fees--', fee) 
                    print('final amt',fee.final_amt)
                    
                    print('stu.feeDisc',fee.feeDisc)                    
                    fee = (fee.final_amount-((fee.final_amount/100)*fee.feeDisc))
                    totalfees =float(fee)                   



                    print('fee--', fee)
                    feeslist.append(fee) 

                print("feeslist--", feeslist)
                mydata = zip(student, feeslist)
                return render(request, 'fees/submitFee.html', {'mydata': mydata, "user": user})

            elif(userAction == 'studentFee'):
                subjectId = request.POST.get('subjectId')
                dataObj = AddStudentInst.objects.get(id=subjectId)
                finalfees = request.POST.get("studentfinalfee",None)
                print('finalfees',finalfees)
                print('dataobj',dataObj.student)
                print('coursename',dataObj.courseName)
                print('forclass',dataObj.forclass)
                print('tachtype',dataObj.teachType)

                addfess = AddFeesC.objects.all()
                for i in addfess:
                    print('i',i)                
                addFeeObj = AddFeesC.objects.filter(Q(courseName = dataObj.courseName) & Q(forclass = dataObj.forclass))
                print('add fee Obj',addFeeObj)                                
                # addFeeObj = AddFeesC.objects.filter(Q(courseName = dataObj.courseName) & Q(forclass = dataObj.forclass) &
                #                                      Q(teachType=dataObj.teachType))
                    # courseName=dataObj.courseName, 
                    # forclass=dataObj.forclass,
                    # teachType=dataObj.teachType                 
                b=[]                
                for i in addFeeObj:
                    a = i.final_amt
                    b.append(a)
                    print('a',a)
                print(b)

                c=float(b[0])
                fee = float(c-((c/100)*10))
                print('fee',fee)
                balancesfis = 0               
                if(addFeeObj):
                    addFeeObj = addFeeObj[0]
                else:
                    return HttpResponse(f"Fees for this subject Combination doesnot Exist! <br>courseName  = {dataObj.courseName},<br>forclass = {dataObj.forclass},<br>teachType = {dataObj.teachType}")
              #  feeObj = dataObj.fees.all()
                feeObj = SubmitFees.objects.all()
                print('feeObj',feeObj)
                # if(not feeObj):
                #     feeObjNew = SubmitFees(
                #         username=dataObj,
                #         subject=addFeeObj.courseName,
                #         totalFee=addFeeObj.final_amount,
                #         balanceFee=addFeeObj.final_amount,
                #         totalInstallments=dataObj.instalment,
                #         instalmentDue=dataObj.instalment
                #     )
                #     print("bs", feeObjNew.instalmentDue)
                #     feeObjNew.save()
                #     feeObj = dataObj.fees.all()                
                                
                instaldue = 0
                totalinstal = 0

                # feeObjNew = SubmitFees(                       
                #         student = dataObj.student,                                           
                #         totalFee = finalfees,
                #         balanceFee= balancesfis ,
                #         feePayed = finalfees,
                #         instalmentDue = instaldue,
                #         totalInstallments = totalinstal,                        
                #     )                    
                # feeObjNew.save()
                
                feeObjNew = SubmitFees(                       
                        student = dataObj.student,                                           
                        totalFee = finalfees,
                        balanceFee= balancesfis ,
                        feePayed = finalfees,
                        instalmentDue = instaldue,
                        totalInstallments = totalinstal,                        
                    )                    
                feeObjNew.save()
                print("bs", feeObjNew.instalmentDue)
                feeObj = SubmitFees.objects.filter( student = dataObj.student)
                print('feeObj',feeObj)
                # for i in feeObj:
                #     print(i.fees)
                feeObj = feeObj[0]
                print('feeobj id',feeObj.id )
                print(feeObj.instalmentDue)
                payment = feeObj.balanceFee
                # try:
                #     payment = feeObj.balanceFee/feeObj.instalmentDue
                # except:
                #     payment = feeObj.balanceFee
                # print(payment)
                
                inputData = {
                    'installmentNumber': feeObj.totalInstallments - feeObj.instalmentDue ,
                    'payment': payment, 
                    'feeId': feeObj.id,
                }
                installmentnotcomplete = (feeObj.instalmentDue != 0)
                return render(
                    request,
                    'fees/submitFee.html',
                    {
                        'inputData': inputData, 'installmentsDone': feeObj.totalInstallments - feeObj.instalmentDue, 'feeObj': feeObj, 'installmentnotcomplete': installmentnotcomplete,'dataObj':dataObj,'finalfees':finalfees
                    }
                )
            elif(userAction == 'submitFee'):
                iNum = int(float(request.POST.get('iNum')))
                fees = int(float(request.POST.get('fees')))
                payed = int(float(request.POST.get('payed')))
                
                feeId = request.POST.get('feeId')

                submitObj = SubmitFees.objects.get(id = feeId)
                a = submitObj.feePayed
                b = a + payed
                d = submitObj.balanceFee 
                e =d - payed
                f = submitObj.instalmentDue
                g = f- 1



                # print(dir(submitObj.feePayed))
                # print(submitObj.feePayed.to_integral_value())
                # submitObj.feePayed = F('feePayed') + payed
                # submitObj.balanceFee = F('balanceFee') - payed
                # submitObj.instalmentDue = F('instalmentDue') - 1
                # submitObj.save()

                
                submitObj.feePayed = b
                submitObj.balanceFee = e
                submitObj.instalmentDue = g
                submitObj.save()
                print("fess payment successfully")
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
        print('archieve id' ,id)
        fees.archieved = True
        fees.save()
        messages.success(request, "Fees Archive Succssfully")
        return redirect("archiveFeeList")
    return HttpResponse("You Are Not Authenticated for this Page")


@login_required(login_url='Login')
def unarchiveFee(request,id):
    if request.session['type']=='Institute':
        user = User.objects.get(username=request.session['user'])
        inst = Institute.objects.get(user=user)         
        fees = AddFeesC.objects.get(id=id)
        print('archieve id' ,id)
        fees.archieved = False
        fees.save()
        messages.success(request, "Fees un archive fees Succssfully")
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
