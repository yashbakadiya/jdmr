from rest_framework import serializers

from .models import NotesInstitute, NotesTutor


class NotesInstituteSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotesInstitute
        fields = "__all__"


class NotesTutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotesTutor
        fields = "__all__"
