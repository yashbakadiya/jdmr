from rest_framework import serializers

from .models import enrollTutors, TutorRatings


class enrollTutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = enrollTutors
        fields = "__all__"
