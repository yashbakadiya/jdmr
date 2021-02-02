from rest_framework import serializers

from .models import BatchTiming, BatchTimingTutor, Notice


class BatchTimingSerializer(serializers.ModelSerializer):
    class Meta:
        model = BatchTiming
        fields = ("batchName",  "days",  "startTime",  "endTime",
                  "original24time",    "institute",  "course",  "forclass")


class BatchTimingTutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = BatchTimingTutor
        fields = ("batchName", "days", "startTime", "endTime",
                  "original24time", "StartDate", "EndDate", "Tutor")


class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = ("title", "description", "batch")
