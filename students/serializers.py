from rest_framework import serializers

from .models import AddStudentInst, School, PostTution, PostAssignment


class AddStudentInstSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddStudentInst
        fields = "__all__"
