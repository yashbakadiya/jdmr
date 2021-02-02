from rest_framework import serializers

from .models import Exam, MultipleQuestion, MultipleAnswer, LongAnswerQuestion, BooleanQuestion, ShortAnswerQuestion, TutorExam, TutorMultipleQuestion, TutorBooleanQuestion, TutorMultipleAnswer, TutorLongAnswerQuestion, TutorShortAnswerQuestion


class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = "__all__"


class MultipleQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MultipleQuestion
        fields = "__all__"


class MultipleAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = MultipleAnswer
        fields = "__all__"


class LongAnswerQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LongAnswerQuestion
        fields = "__all__"


class BooleanQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BooleanQuestion
        fields = "__all__"


class ShortAnswerQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortAnswerQuestion
        fields = "__all__"


class TutorExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = TutorExam
        fields = "__all__"


class TutorMultipleQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TutorMultipleQuestion
        fields = "__all__"


class TutorMultipleAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = TutorMultipleAnswer
        fields = "__all__"


class TutorLongAnswerQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TutorLongAnswerQuestion
        fields = "__all__"


class TutorBooleanQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TutorBooleanQuestion
        fields = "__all__"


class TutorShortAnswerQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TutorShortAnswerQuestion
        fields = "__all__"
