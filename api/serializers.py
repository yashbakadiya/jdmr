from rest_framework import serializers
from tutor.models import *


class SignupCoachingCenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = SignupCoachingCentre
        fields = "__all__"

class CoachingCenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoginCoachingCentre
        fields = "__all__"

class SignupTutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = SignupTutor
        fields = "__all__"

class SignupStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SignupStudent
        fields = "__all__"

class CoachingCenterCoursesSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddCourses
        fields = "__all__"

class CoachingCenterCoursesArchivedSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArchiveCourses
        fields = "__all__"

class CoachingCenterTeachingTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeachingType
        fields = "__all__"

class CoachingCenterBatchTimingSerializer(serializers.ModelSerializer):
    class Meta:
        model = BatchTiming
        fields = "__all__"

class CoachingCenterFeesSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddFeesC
        fields = "__all__"

class CoachingCenterArchiveFeesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArchiveFees
        fields = "__all__"

class CoachingCenterAddStudentInstSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddStudentInst
        fields = "__all__"

class CoachingCenterenrollTutorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = enrollTutors
        fields = "__all__"


class CoachingCenterArchiveTutorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArchiveTutors
        fields = "__all__"

class CoachingCenterAddStudentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddStudentDetail
        fields = "__all__"

class CoachingCenterArchiveStudentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArchiveStudents
        fields = "__all__"

class CoachingCenterTutorialInstituteSerializer(serializers.ModelSerializer):
    class Meta:
        model = TutorialInstitute
        fields = "__all__"

class CoachingCenterExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = "__all__"

class CoachingCenterNotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotesInstitute
        fields = "__all__"

class SignupStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentMapping
        fields = "__all__"

class SignupStudentExamResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentExamResult
        fields = "__all__"

class SignupStudentExamAnswersSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentAnswer
        fields = "__all__"

class SignupStudentShortAnswerQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortAnswerQuestion
        fields = "__all__"

class SignupStudentBooleanAnswerQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BooleanQuestion
        fields = "__all__"

class SignupStudentLongAnswerQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LongAnswerQuestion
        fields = "__all__"

class SignupStudentMultipleAnswerQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MultipleQuestion
        fields = "__all__"

class SignupStudentPostTuitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostTution
        fields = "__all__"

class SignupStudentPostAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostAssignment
        fields = "__all__"

class TutorAddTutorialSerializer(serializers.ModelSerializer):
    class Meta:
        model = TutorialTutors
        fields = "__all__"

class TutorBatchTimingSerializer(serializers.ModelSerializer):
    class Meta:
        model = BatchTimingTutor
        fields = "__all__"

class TutorAddNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotesTutor
        fields = "__all__"

class StudentExamResultSerializer(serializers.ModelSerializer):
	exam_name = serializers.ReadOnlyField(source='ExamName')
	course = serializers.ReadOnlyField(source='ExamCourse')
	exam_date = serializers.ReadOnlyField(source='ExamDate')
	class Meta:
		model = StudentExamResult
		fields = "__all__"

class StudentMappingSerializer(serializers.ModelSerializer):
	exam_name = serializers.ReadOnlyField(source='ExamName')
	course = serializers.ReadOnlyField(source='ExamCourse')
	exam_date = serializers.ReadOnlyField(source='ExamDate')
	status = serializers.ReadOnlyField(source='Status')
	duration = serializers.ReadOnlyField(source='ExamDuration')
	total_Question = serializers.ReadOnlyField(source='total_questions')
	class Meta:
		model = StudentMapping
		fields = "__all__"

## Tutorials Review

class TutorTutorialsReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewsTutor
        fields = "__all__"

class CenterTutorialsReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewsInstitute
        fields = "__all__"

## Institute Reviews and Tutor Reviews

class TutorReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TutorRatings
        fields = "__all__"

class CenterReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstituteRatings
        fields = "__all__"

class SignupStudentAnswersAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentAnswer
        fields = "__all__"