from rest_framework import serializers

from .models import Courses, TeachingType


class CoursesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courses
        fields = ('courseID', 'courseName', 'forclass', 'intitute')


class TeachingTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeachingType
        fields = "__all__"
