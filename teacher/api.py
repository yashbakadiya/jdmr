from django.http import response
from django.shortcuts import render, redirect, HttpResponse
from .models import enrollTutors, TutorRatings
from courses.models import Courses, TeachingType
from accounts.models import Institute, Teacher, Student
from django.contrib.auth.models import User
import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from .serializers import enrollTutorSerializer
from accounts.serializers import TeacherSerializer, UserSerializer
from django.core import serializers
from django.db.models import Q
from datetime import datetime, timedelta


# NEEDs Teacher App Model
# Needed Parameters 'type', 'username',
# GET Parameters
# 'archive-list'(optional)
# POST Parameters
# 'firstName', 'lastName', 'email', 'phone', 'loc'
# 'ctn_combined', 'cn_combined', 'ttn_combined', 'availability'
# PUT Parameters
# 'pk', 'availability', "NewUsername", "NewEmail",
# "NewPassword", "NewPhone" 'ctn_combined', 'cn_combined', 'ttn_combined'
# # DELETE Parameters
# 'pk' <-- EnrollTutor ID
@api_view(["POST", "GET", "PATCH", "DELETE"])
def TutorAPI(request):
    data = request.data
    if data['type'] == "Institute":
        user = User.objects.get(username=data['username'])
        inst = Institute.objects.get(user=user)
        if request.method == "GET":
            tutors = enrollTutors.objects.filter(
                institute=inst, archieved=False)
            courses = Courses.objects.filter(intitute=inst, archieved=False)
            courselist = []
            for course in courses:
                for tutor in tutors:
                    if int(tutor.courseName) == course.id:
                        courselist.append(course.courseName)
            tutors = zip(tutors, courselist)
            if 'archive_list' in data:
                archive_list = data['archive_list']
                for x in archive_list:
                    arTutor = enrollTutors.objects.get(id=int(x))
                    arTutor.archieved = True
                    arTutor.save()
                data['success'] = "Teacher Added To Archieve Successfully"
                return Response(data)
            data['tutors'] = tutors
            data['success'] = "DAta fetched successfully"
            return Response(data)
        elif request.method == "POST":
            firstName = data['firstName']
            lastName = data['lastName']
            email = data['email']
            phone = data['phone']
            password = phone
            username = email
            location = data['loc']
            error = {}
            if firstName.isalpha() == False | lastName.isalpha() == False:
                error['name-error'] = "Name must be alphabetical"
            if len(phone) != 10:
                error['phone-error'] = "Phone Number must be 10 digits"
            if phone.isdigit() == False:
                error['phone-error-2'] = "Phone Number must be numeric"
            if User.objects.filter(email=email).exists():
                error['email-error'] = "Email Already Exists"
            if Teacher.objects.filter(phone=phone).exists():
                error['phone-error-3'] = "Phone No is Already Registered"
            if(len(error) > 0):
                data['errors'] = error
                return Response(data)
            else:
                user2 = User(username=username, email=email, password=password,
                             first_name=firstName, last_name=lastName)
                user2.save()
                teacher = Teacher(user=user2, address=location, phone=phone)
                teacher.save()
                ctn = data['ctn_combined']
                cn = data['cn_combined']
                ttn = data['ttn_combined']
                ttn = [x.replace("\r", "") for x in ttn]
                availability = data['availability']
                if(availability == 'weekly'):
                    availability = 1
                elif(availability == 'weekend'):
                    availability = 2
                elif(availability == 'both'):
                    availability = 3
                else:
                    data['availability-error'] = 'availability error'
                    availability = 0
                for x in range(len(ttn)):
                    addTeacher = enrollTutors(
                        forclass=cn[x], teachType=ttn[x], courseName=ctn[x], institute=inst, teacher=teacher, availability=availability)
                    addTeacher.save()
                data['success'] = "Teacher Added Successfully"
                return Response(data)
        elif request.method == "PATCH":
            pk = data['pk']
            editTutorObj = enrollTutors.objects.get(pk=pk)
            teacher = Teacher.objects.get(
                user__username=editTutorObj.teacher.user.username)
            data = TeachingType.objects.values_list(
                'courseID', 'forclass', 'teachType', 'course')
            processed_data = {}
            for x in data:
                processed_data[x[0]] = [x[1].split(", "), x[2].split("\n")]

            availability = data['availability']
            if availability == "weekly":
                availability = 1
            elif availability == "weekend":
                availability = 2
            elif availability == "both":
                availability = 3
            else:
                availability = 0
            NewUsername = data["NewUsername"]
            NewEmail = data["NewEmail"]
            NewPassword = data["NewPassword"]
            NewPhone = data["NewPhone"]
            teacher.name = NewUsername
            teacher.email = NewEmail
            teacher.password = NewPassword
            teacher.phone = NewPhone
            teacher.save()
            user = User.objects.get(
                username=editTutorObj.teacher.user.username)
            user.username = NewUsername
            user.password = NewPassword
            user.email = NewEmail
            user.save()
            editTutorObj.courseName = data['ctn_combined']
            editTutorObj.forclass = data['cn_combined']
            editTutorObj.teachType = data['ttn_combined']
            editTutorObj.teacher = teacher
            editTutorObj.availability = availability
            editTutorObj.save()
            data['success'] = "Teacher Updated Successfully"
            return Response(data)
        elif request.method == "DELETE":
            pk = data["pk"]
            et = enrollTutors.objects.get(pk=pk)
            et.delete()
            data['success'] = "Teacher Deleted Successfully"
            return Response(data)
    data['error'] = "You Are Not Authenticated"
    return Response(data)


@api_view(["POST", "GET"])
def SearchTutorAPI(request):
    data = request.data
    if data['type'] == "Institute":
        searchKeyword = data['searchkeyword']
        if searchKeyword:
            teacher = Teacher.objects.filter(Q(user__username__icontains=searchKeyword) | Q(
                user__email__icontains=searchKeyword))
            if teacher:
                data['teacher'] = teacher
                return Response(data)
        data['error'] = 'no result found'
        return Response(data)
    data['error'] = "You Are Not Authenticated"
    return Response(data)


def enrolledTutorsObjectToDict(obj):
    data = {
        'id': obj.id,
        'username': obj.user.username,
        'firstName': obj.user.first_name,
        'lastName': obj.user.last_name,
        'email': obj.user.email,
        'address': obj.address,
        'phone': obj.phone,
        'availability': obj.availability,
        'qualification': obj.qualification,
        'experience': obj.experiance,
        'gender': obj.gender,
        'fees': obj.fees,
        'forclass': obj.forclass
    }
    courseID = obj.course.replace(";", '')
    courseID = list(set(courseID))
    courses = []
    for i in courseID:
        course = Courses.objects.get(id=i)
        courses.append(course.courseName)
    data['courseName'] = courses
    return data


@api_view(["POST", "GET"])
def EnrolledTutorAPI(request):
    data = request.data
    if request.method == "POST":
        className = data['className']
        classlist = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII',
                     'VIII', 'IX', 'X', 'XI', 'XII', 'Others', 'Nursery']
        if int(className):
            className = classlist[int(className)-1]
        loc = data['loc']
        teachtype = data['tutortype']
        subject = data['subject']
        budget = data['budget']
        la1 = data['cityLat']
        lo1 = data['cityLng']
        fees = data['fees']
        tutortype = data['tutortype']
        print(request.POST)
        searchQuery = Teacher.objects.filter(Q(forclass__icontains=className) or Q(
            fees < budget) or Q(address__icontains=loc) or Q(availability=tutortype))
        allData = searchQuery
        jsonData = []
        for x in allData:
            jsonData.append(enrolledTutorsObjectToDict(x))
        data['allData'] = allData
        data['jsonData'] = jsonData
        return Response(data)
    elif request.method == "GET":
        allData = Teacher.objects.all()
        jsonData = []
        for x in allData:
            jsonData.append(enrolledTutorsObjectToDict(x))
        data['allData'] = allData
        data['jsonData'] = jsonData
        return Response(data)
    return Response(data)


@api_view(["POST", "GET"])
def ReviewTutorAPI(request):
    data = request.data
    if request.session['type'] == "Student":
        tutor_id = data['tutor_id']
        user = User.objects.get(username=data['username'])
        student = Student.objects.get(user=user)
        tutor = Teacher.objects.get(id=tutor_id)
        reviews = TutorRatings.objects.filter(Tutor=tutor)
        currentStudent = True
        if TutorRatings.objects.filter(Q(Student=student) and Q(Tutor=tutor)).exists():
            currentStudent = False
        count = reviews.count()
        sumRating = 0
        for i in reviews:
            add = i.Rating
            sumRating += add
        try:
            avgRating = sumRating/count
        except:
            avgRating = 0
        data['i'] = tutor
        data['reviews'] = reviews
        data['avgRating'] = range(int(avgRating))
        data['currentStudent'] = currentStudent
        if request.method == "POST" and not(TutorRatings.objects.filter(Q(Student=student) and Q(Tutor=tutor)).exists()):
            rating = data["rating"]
            comment = data["comment"]
            print(rating, comment)
            tr = TutorRatings(
                Tutor=tutor,
                Student=student,
                Review=comment,
                Rating=rating)
            tr.save()
        return Response(data)
