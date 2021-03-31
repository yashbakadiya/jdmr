from rest_framework import serializers

from .models import (
    BuyInstituteNotes,
    BuyInstituteTutorial,
    BuyTutorExam,
    BuyTutorNotes,
    BuyTutorTutorial)


class BuyInstituteNotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuyInstituteNotes
        fields = ('student', 'note', 'status')

class BuyTutorNotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuyTutorNotes
        fields = ('student', 'note', 'status')


class BuyTutorTutorialSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuyTutorTutorial
        fields = ('student', 'tutorial', 'status')


class BuyInstituteTutorialSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuyInstituteTutorial
        fields = ('student', 'tutorial', 'status')

class BuyTutorExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuyTutorExam
        fields = ('student', 'exam', 'status')

