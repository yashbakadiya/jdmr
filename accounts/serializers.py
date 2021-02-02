from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Institute, Teacher, Student


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'first_name', 'last_name', 'email')


class InstituteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institute
        fields = ['user', "address", "phone"]


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['user', "address", "phone"]


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['user', "address", "phone"]
