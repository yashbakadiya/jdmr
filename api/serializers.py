from rest_framework import serializers
from tutor.models import *



class CoachingCenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoginCoachingCentre
        fields = ['username', 'password',]