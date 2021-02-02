from django.shortcuts import render, redirect, HttpResponse
from .models import School, AddStudentInst, PostAssignment, PostTution
from courses.models import Courses, TeachingType
from accounts.models import Institute, Teacher, Student
from django.contrib.auth.models import User
import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from .serializers import AddStudentInstSerializer
from django.core import serializers
from django.db.models import Q
from datetime import datetime, timedelta
from batches.models import BatchTiming
from json import dumps


@api_view(["POST", "GET"])
def AddStudentInstAPI(request):
    data = request.data
    if request.session['type'] == "Institute":
        user = User.objects.get(username=data['user'])
        inst = Institute.objects.get(user=user)
        if request.method == "POST":
            firstName = data['firstName']
            lastName = data['lastName']
            email = data['email']
            username = email
            phone = data['phone']
            password = phone
            schoolName = data['schoolName']
            lat = data['cityLat']
            lng = data['cityLng']
            if firstName.isalpha() == False | lastName.isalpha() == False | schoolName.isalpha() == False:
                data['error'] = "Name must be alphabetical"
                return Response(data)
            if len(phone) != 10:
                data['error'] = "Phone Number must be 10 digits"
                return Response(data)
            if Student.objects.filter(user__email=email).exists():
                data['error'] = "Student with This Email Exists"
                return Response(data)
            if Student.objects.filter(phone=phone).exists():
                data['error'] = "Phone Number is Already Registered"
                return Response(data)
            user = User(
                username=username,
                first_name=firstName,
                last_name=lastName,
                email=email,
                password=password,
            )
            user.save()
            student = Student(user=user, phone=phone,
                              address=schoolName, schoolName=schoolName)
            student.save()
            if School.objects.filter(name=schoolName).exists():
                pass
            else:
                school = School(name=schoolName)
                school.save()
            ctn = data['ctn_combined']
            cn = data['cn_combined']
            ttn = data['ttn_combined']
            ttn = [x.replace("\r", "") for x in ttn]
            batchName = data['batchN_combined']
            feeDis = data['feedis_combined']
            installments = data['noi_combined']
            for x in range(len(ttn)):
                try:
                    temp = float(feeDis[x])
                except:
                    try:
                        temp = int(feeDis[x])
                    except:
                        temp = 0
                addstudent = AddStudentInst(
                    student=student,
                    institute=inst,
                    courseName=ctn[x],
                    forclass=cn[x],
                    teachType=ttn[x],
                    batch=batchName[x],
                    feeDisc=temp,
                    installments=installments[x]
                )
                addstudent.save()
            data['success'] = "Student Added Successfully"
            return Response(data)
        else:
            schools = School.objects.all()
            school_list = list(map(str, schools))
            data = TeachingType.objects.filter(course__intitute__user=user).values_list(
                'courseID', 'forclass', 'teachType', 'course')
            print('data--', data)
            processed_data = {}
            for x in data:
                processed_data[x[0]] = [x[1].split(", "), x[2].split("\n")]
            data['data'] = TeachingType.objects.filter(
                course__intitute__user=user)
            data['jsdata'] = dumps(processed_data)
            data['school_list'] = school_list
            data['batch'] = BatchTiming.objects.filter(institute=inst)
            return Response(data)


@api_view(["POST", "GET"])
def ViewStudentInstAPI(request):
    data = request.data
    if request.session['type'] == "Institute":
        user = User.objects.get(username=data['user'])
        inst = Institute.objects.get(user=user)
        if request.method == "POST":
            archiveList = data['archive-list']
            for x in archiveList:
                arStudent = AddStudentInst.objects.get(id=int(x))
                arStudent.archieved = True
                arStudent.save()
            data['success'] = "Student Added To Archieve Successfully"
            return Response(data)
        else:
            students = AddStudentInst.objects.filter(
                institute=inst, archieved=False)
            courses = []
            for student in students:
                course = Courses.objects.get(id=int(student.courseName))
                courses.append(course)
            students = zip(students, courses)
            data['students'] = students
            return Response(data)
    data['error'] = "Not Authenticated!"
    return Response(data)


@api_view(["DELETE"])
def DeleteStudentInstAPI(request):
    data = request.data
    if request.session['type'] == "Institute":
        user = User.objects.get(username=data['user'])
        inst = Institute.objects.get(user=user)
        pk = data['pk']
        try:
            delStu = AddStudentInst.objects.get(pk=pk)
            delStu.delete()
            data['success'] = "Student Deleted Successfully"
            return Response(data)
        except:
            data['error'] = "Student Id Does Not Exist"
            return Response(data)
    data['error'] = "Not Authenticated!"
    return Response(data)


@api_view(["POST", "GET"])
def ArchiveStudentInstAPI(request):
    data = request.data
    if request.session['type'] == "Institute":
        user = User.objects.get(username=data['user'])
        inst = Institute.objects.get(user=user)
        if request.method == "POST":
            archiveList = data['archive-list']
            for x in archiveList:
                arStudent = AddStudentInst.objects.get(id=int(x))
                arStudent.archieved = False
                arStudent.save()
            data["success"] = "Student Removed From Archieve Successfully"
            return Response(data)
        else:
            students = AddStudentInst.objects.filter(
                institute=inst, archieved=True)
            data['students'] = students
            return Response(data)
    data['error'] = "Not Authenticated!"
    return Response(data)


@api_view(["PUT", "GET"])
def EditStudentAPI(request):
    data = request.data
    if data['type'] == "Institute":
        user = User.objects.get(username=data['user'])
        inst = Institute.objects.get(user=user)
        schools = School.objects.all()
        school_list = list(map(str, schools))
        data = TeachingType.objects.filter(course__intitute__user=user).values_list(
            'courseID', 'forclass', 'teachType', 'course')
        processed_data = {}
        for x in data:
            processed_data[x[0]] = [x[1].split(", "), x[2].split("\n")]
        student = AddStudentInst.objects.get(id=data['student-id'])
        courses = Courses.objects.filter(intitute=inst)
        data.update({
            'stfname': student.student.user.first_name,
            'stlname': student.student.user.last_name,
            'stemail': student.student.user.email,
            'stphone': student.student.phone,
            'address': student.student.address,
            'schoolName': student.student.schoolName,
            'courses': courses,
            'qry': student,
            "data": TeachingType.objects.filter(course__intitute__user=user),
            "jsdata": dumps(processed_data),
            "school_list": school_list,
            'batch': BatchTiming.objects.filter(institute=inst),
        })
        if request.method == "PUT":
            phone = data['phone']
            schoolName = data['schoolName']
            ctn = data['ctn_combined']
            cn = data['cn_combined']
            ttn = data['ttn_combined']
            ttn = [x.replace("\r", "") for x in ttn]
            batchName = data['batchN_combined']
            feeDis = data['feedis_combined']
            installments = data['noi_combined']
            user = User.objects.get(username=student.student.user.username)
            studentOBJ = Student.objects.get(user=user)
            user.password = phone
            user.save()
            studentOBJ.user = user
            studentOBJ.phone = phone
            studentOBJ.address = data["loc"]
            studentOBJ.schoolName = schoolName
            studentOBJ.save()
            for x in range(len(ttn)):
                try:
                    temp = float(feeDis[x])
                except:
                    try:
                        temp = int(feeDis[x])
                    except:
                        temp = 0
                student.student = studentOBJ
                student.courseName = ctn[x]
                student.forclass = cn[x]
                student.teachType = ttn[x]
                student.batch = batchName[x]
                student.feeDisc = temp
                student.installments = installments[x]
                student.save()
            data['success'] = "Student Updated Successfully"
            return Response(data)
        return Response(data)
    data['error'] = "Not Authenticated!"
    return Response(data)


@api_view(["POST", "GET"])
def SearchUserStudentAPI(request):
    data = request.data
    if data['type'] == "Institute":
        user = User.objects.get(username=data['user'])
        inst = Institute.objects.get(user=user)
        if request.method == "POST":
            print(request.POST)
            srch = data['search-keyword']
            if srch:
                match = Student.objects.filter(
                    Q(user__username__icontains=srch) | Q(user__email__icontains=srch))
                if len(match):
                    data['search-result'] = match
                    data['success'] = "Search is Successfull"
                    return Response(data)
                else:
                    data['error'] = 'no result found'
                    return Response(data)
        else:
            data['error'] = "Request is not POST"
            return Response(data)
    data['error'] = "Not Authenticated!"
    return Response(data)


@api_view(["POST", "GET"])
def AddalreadyExistsStudentAPI(request):
    data = request.data
    if data['type'] == "Institute":
        id = data['student-id']
        student = Student.objects.get(id=id)
        user = User.objects.get(username=data['user'])
        inst = Institute.objects.get(user=user)
        if request.method == "POST":
            ctn = data['ctn_combined']
            cn = data['cn_combined']
            ttn = data['ttn_combined']
            ttn = [x.replace("\r", "") for x in ttn]
            batchName = data['batchN_combined']
            feeDis = data['feedis_combined']
            installments = data['noi_combined']
            for x in range(len(ttn)):
                try:
                    temp = float(feeDis[x])
                except:
                    try:
                        temp = int(feeDis[x])
                    except:
                        temp = 0
                addstudent = AddStudentInst(
                    student=student,
                    institute=inst,
                    courseName=ctn[x],
                    forclass=cn[x],
                    teachType=ttn[x],
                    batch=batchName[x],
                    feeDisc=temp,
                    installments=installments[x]
                )
                addstudent.save()
            data['success'] = "Student Added Successfully"
            return Response(data)
        else:
            schools = School.objects.all()
            school_list = list(map(str, schools))
            data = TeachingType.objects.filter(course__intitute__user=user).values_list(
                'courseName', 'forclass', 'teachType')
            processed_data = {}
            for x in data:
                processed_data[x[0]] = [x[1].split(", "), x[2].split("\n")]
            data.update({
                "data": TeachingType.objects.filter(course__intitute__user=user),
                "student": student,
                "jsdata": dumps(processed_data),
                "school_list": school_list,
                'batch': BatchTiming.objects.filter(institute=inst)
            })
            return Response(data)
    data['error'] = "Not Authenticated!"
    return Response(data)


@api_view(["POST", "GET"])
def PostAssignmentAPI(request):
    data = request.data
    if data['type'] == "Student":
        user = User.objects.get(username=data['username'])
        student = Student.objects.get(user=user)
        courseID = data['ctn']
        course = Courses.objects.get(id=int(courseID))
        if request.method == "POST":

            postAssigObj = PostAssignment(
                student=student,
                courseName=course.courseName,
                forclass=data['cn'],
                description=data['description'],
                descriptionFile=data['file'],
                requirement=data['requirement'],
                budget=data['budget']
            )
            postAssigObj.save()
            data['success'] = "Data Saved!"
            return Response(data)
        else:
            data1 = Courses.objects.values_list('id', 'forclass', 'courseName')
            processed_data = {}
            for x in data1:
                processed_data[x[0]] = [x[1].split(", "), x[2].split("\n")]
            data.update({
                "data": Courses.objects.all(),
                "jsdata": dumps(processed_data)
            })
            return Response(data)
    data['error'] = "Not Authenticated!"
    return Response(data)


@api_view(["POST", "GET"])
def PostTutionAPI(request):
    data = request.data
    if data['type'] == "Student":
        if request.method == "POST":
            data = Courses.objects.values_list('id', 'forclass', 'courseName')
            processed_data = {}
            for x in data:
                processed_data[x[0]] = [x[1].split(", "), x[2].split("\n")]
            data.update({
                "data": Courses.objects.all(),
                "jsdata": dumps(processed_data),
                "success": "Data Added"
            })
            return Response(data)
        else:
            data['error'] = "Request is not POST"
            return Response(data)
    data['error'] = "Not Authenticated!"
    return Response(data)


@api_view(["POST", "GET"])
def ViewAssignmentAPI(request):
    data = request.data
    if data['type'] == "Student":
        if request.method == "POST":
            delteSno = data['delteSno']
            try:
                PostAssignment.objects.get(sno=delteSno).delete()
            except Exception as e:
                data['error'] = e
                return Response(data)
            data['success'] = "Assignment Deleted"
            return Response(data)

        else:
            user = User.objects.get(username=data['username'])
            student = Student.objects.get(user=user)
            data['data'] = student
            return Response(data)
    data['error'] = "Not Authenticated!"
    return Response(data)


@api_view(["POST", "GET"])
def ViewTutionAPI(request):
    data = request.data
    if data['type'] == "Student":
        if request.method == "POST":
            delteSno = data['delteSno']
            try:
                PostTution.objects.get(sno=delteSno).delete()
            except Exception as e:
                data['error'] = e
                return Response(data)
            data['success'] = "Tution Deleted"
            return Response(data)
        else:
            user = User.objects.get(username=data['username'])
            student = Student.objects.get(user=user)
            data['data'] = student
            return Response(data)
    data['error'] = "Not Authenticated!"
    return Response(data)
