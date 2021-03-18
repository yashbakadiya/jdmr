from django.db import models
from accounts.models import Institute, Teacher, Student
from courses.models import Courses
from django.urls import reverse
# Create your models here.


class Exam(models.Model):
    institute = models.ForeignKey(
        Institute, related_name='centername', on_delete=models.CASCADE)
    course = models.ForeignKey(
        Courses, related_name="exams", on_delete=models.CASCADE)
    Class = models.CharField(max_length=20)
    Batch = models.CharField(max_length=100)
    Name = models.CharField(max_length=200)
    exam_date = models.DateField()
    exam_time = models.TimeField(blank=True, null=True)
    exam_duration = models.IntegerField(default=0)
    timezone = models.CharField(max_length=200)
    pass_percentage = models.IntegerField()
    reexam_date = models.DateField(blank=True, null=True)
    calculator = models.BooleanField(default=False)
    imgupload = models.BooleanField(default=False)
    negative_marking = models.BooleanField(
        default=False, blank=True, null=True)
    negative_marks = models.FloatField(blank=True, null=True)
    tandc = models.TextField()
    status = models.BooleanField(default=False)
    resultonmail = models.BooleanField(default=False, blank=True, null=True)
    question_count = models.IntegerField(default=0)

    def __str__(self):
        return self.Name


class MultipleQuestion(models.Model):
    exam = models.ForeignKey(
        Exam, related_name='multiple_question', on_delete=models.CASCADE)
    question = models.TextField()
    correct_ans = models.CharField(max_length=1000)
    marks = models.FloatField()
    question_no = models.IntegerField(default=0)
    level = models.CharField(max_length=100, default='medium')
    negative_marks = models.FloatField(default=0)
    section = models.CharField(max_length=10, default='A')

    def __str__(self):
        return self.question

    @property
    def Delete_url(self):
        return reverse('multipleansdelete', args=(self.id,))

    @property
    def Edit_url(self):
        return reverse('multipleansedit', args=(self.id,))

    @property
    def Edit_Tutor(self):
        return reverse('multipleansedittutor', args=(self.id,))


class MultipleAnswer(models.Model):
    question = models.ForeignKey(
        MultipleQuestion, on_delete=models.CASCADE, related_name='options')
    option = models.CharField(max_length=150)

    def __str__(self):
        return f'{self.question.question} - {self.option}'


class LongAnswerQuestion(models.Model):
    exam = models.ForeignKey(
        Exam, related_name='subjective_question', on_delete=models.CASCADE)
    question = models.TextField()
    level = models.CharField(max_length=100, default='medium')
    correct_ans = models.TextField(max_length=350)
    marks = models.FloatField()
    question_no = models.IntegerField(default=0)
    negative_marks = models.FloatField()
    section = models.CharField(max_length=10)

    def __str__(self):
        return self.question

    @property
    def Delete_url(self):
        return reverse('longansdelete', args=(self.id,))

    @property
    def Edit_url(self):
        return reverse('longansedit', args=(self.id,))

    @property
    def Edit_Tutor(self):
        return reverse('longansedittutor', args=(self.id,))


class BooleanQuestion(models.Model):
    exam = models.ForeignKey(
        Exam, related_name='boolean_question', on_delete=models.CASCADE)
    question = models.TextField()
    option1 = models.CharField(max_length=1000, null=True, blank=True)
    option2 = models.CharField(max_length=1000, null=True, blank=True)
    correct_ans = models.CharField(max_length=1000)
    marks = models.FloatField()
    question_no = models.IntegerField(default=0)
    level = models.CharField(max_length=100, default='medium')
    negative_marks = models.FloatField()
    section = models.CharField(max_length=10)

    def __str__(self):
        return self.question

    @property
    def Delete_url(self):
        return reverse('booleanansdelete', args=(self.id,))

    @property
    def Edit_url(self):
        return reverse('booleanansedit', args=(self.id,))

    @property
    def Edit_Tutor(self):
        return reverse('booleanansedittutor', args=(self.id,))


class ShortAnswerQuestion(models.Model):
    exam = models.ForeignKey(
        Exam, related_name='oneline_question', on_delete=models.CASCADE)
    question = models.TextField()
    correct_ans = models.TextField(max_length=150)
    marks = models.FloatField()
    question_no = models.IntegerField(default=0)
    level = models.CharField(max_length=100, default='medium')
    negative_marks = models.FloatField()
    section = models.CharField(max_length=10)

    def __str__(self):
        return self.question

    @property
    def Delete_url(self):
        return reverse('shortansdelete', args=(self.id,))

    @property
    def Edit_url(self):
        return reverse('shortansedit', args=(self.id,))

    @property
    def Edit_Tutor(self):
        return reverse('shortansedittutor', args=(self.id,))


class TutorExam(models.Model):
    tutor = models.ForeignKey(
        Teacher, related_name='teacher', on_delete=models.CASCADE)
    courseName = models.CharField(max_length=100,default="")
    forclass = models.CharField(max_length=255,default="")
    Name = models.CharField(max_length=200)
    price = models.IntegerField()
    exam_date = models.DateField()
    exam_time = models.TimeField(blank=True, null=True)
    exam_duration = models.IntegerField(default=0)
    timezone = models.CharField(max_length=200)
    pass_percentage = models.IntegerField()
    reexam_date = models.DateField(blank=True, null=True)
    calculator = models.BooleanField(default=False)
    imgupload = models.BooleanField(default=False)
    negative_marking = models.BooleanField(
        default=False, blank=True, null=True)
    negative_marks = models.FloatField(blank=True, null=True)
    tandc = models.TextField()
    status = models.BooleanField(default=False)
    resultonmail = models.BooleanField(default=False, blank=True, null=True)
    question_count = models.IntegerField(default=0)

    def __str__(self):
        return self.Name


class TutorMultipleQuestion(models.Model):
    exam = models.ForeignKey(
        TutorExam, related_name='multiple_question', on_delete=models.CASCADE)
    question = models.TextField()
    correct_ans = models.CharField(max_length=1000)
    marks = models.FloatField()
    question_no = models.IntegerField(default=0)
    level = models.CharField(max_length=100, default='medium')
    negative_marks = models.FloatField(default=0)
    section = models.CharField(max_length=10, default='A')

    def __str__(self):
        return self.question

    @property
    def Delete_url(self):
        return reverse('multipleansdelete', args=(self.id,))

    @property
    def Edit_url(self):
        return reverse('multipleansedit', args=(self.id,))

    @property
    def Edit_Tutor(self):
        return reverse('multipleansedittutor', args=(self.id,))


class TutorMultipleAnswer(models.Model):
    question = models.ForeignKey(
        TutorMultipleQuestion, on_delete=models.CASCADE, related_name='options')
    option = models.CharField(max_length=150)

    def __str__(self):
        return f'{self.question.question} - {self.option}'


class TutorLongAnswerQuestion(models.Model):
    exam = models.ForeignKey(
        TutorExam, related_name='subjective_question', on_delete=models.CASCADE)
    question = models.TextField()
    level = models.CharField(max_length=100, default='medium')
    correct_ans = models.TextField(max_length=350)
    marks = models.FloatField()
    question_no = models.IntegerField(default=0)
    negative_marks = models.FloatField()
    section = models.CharField(max_length=10)

    def __str__(self):
        return self.question

    @property
    def Delete_url(self):
        return reverse('longansdelete', args=(self.id,))

    @property
    def Edit_url(self):
        return reverse('longansedit', args=(self.id,))

    @property
    def Edit_Tutor(self):
        return reverse('longansedittutor', args=(self.id,))


class TutorBooleanQuestion(models.Model):
    exam = models.ForeignKey(
        TutorExam, related_name='boolean_question', on_delete=models.CASCADE)
    question = models.TextField()
    option1 = models.CharField(max_length=1000, null=True, blank=True)
    option2 = models.CharField(max_length=1000, null=True, blank=True)
    correct_ans = models.CharField(max_length=1000)
    marks = models.FloatField()
    question_no = models.IntegerField(default=0)
    level = models.CharField(max_length=100, default='medium')
    negative_marks = models.FloatField()
    section = models.CharField(max_length=10)

    def __str__(self):
        return self.question

    @property
    def Delete_url(self):
        return reverse('booleanansdelete', args=(self.id,))

    @property
    def Edit_url(self):
        return reverse('booleanansedit', args=(self.id,))

    @property
    def Edit_Tutor(self):
        return reverse('booleanansedittutor', args=(self.id,))


class TutorShortAnswerQuestion(models.Model):
    exam = models.ForeignKey(
        TutorExam, related_name='oneline_question', on_delete=models.CASCADE)
    question = models.TextField()
    correct_ans = models.TextField(max_length=150)
    marks = models.FloatField()
    question_no = models.IntegerField(default=0)
    level = models.CharField(max_length=100, default='medium')
    negative_marks = models.FloatField()
    section = models.CharField(max_length=10)

    def __str__(self):
        return self.question

    @property
    def Delete_url(self):
        return reverse('shortansdelete', args=(self.id,))

    @property
    def Edit_url(self):
        return reverse('shortansedit', args=(self.id,))

    @property
    def Edit_Tutor(self):
        return reverse('shortansedittutor', args=(self.id,))

class StudentMapping(models.Model):
    student = models.ForeignKey(Student, related_name='student_mapping',
                                on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam,related_name='student_exam',on_delete=models.CASCADE)
    course = models.ForeignKey(Courses,related_name="student_course",on_delete=models.CASCADE)


    def __str__(self):
        return str(self.student)
    
    @property
    def Status(self):
        mapping = StudentMapping.objects.get(id=self.id)
        statues = StudentExamResult.objects.filter(student=mapping,exam = self.exam).first()
        return statues.attempted

    @property
    def PassStatus(self):
        mapping = StudentMapping.objects.get(id=self.id)
        statues = StudentExamResult.objects.filter(student=mapping,exam = self.exam).first()
        return statues.pass_status
    
    @property
    def ExamName(self):
        return self.exam.Name
    
    @property
    def ExamCourse(self):
        return self.exam.course.courseName

    @property
    def ExamDate(self):
        return self.exam.exam_date

    @property
    def ExamDuration(self):
        return self.exam.exam_duration

    @property
    def total_questions(self):
        return self.exam.question_count


class StudentExamResult(models.Model):
    student = models.ForeignKey(
        StudentMapping, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    marks_scored = models.FloatField(default=0)
    total_marks = models.FloatField(default=0)
    total_questions = models.IntegerField(default=0)
    attempted = models.BooleanField(default=False)
    percentage = models.CharField(max_length=10, default="10")
    pass_status = models.BooleanField(default=False)
    time_taken = models.CharField(max_length=100, default=0)

    def __str__(self):
        return self.exam.Name

    @property
    def ExamName(self):
        return self.exam.Name
    
    @property
    def ExamCourse(self):
        return self.exam.course.courseName

    @property
    def ExamDate(self):
        return self.exam.exam_date

class StudentAnswer(models.Model):
    student = models.ForeignKey(
        StudentMapping, on_delete=models.CASCADE, blank=True, null=True)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    qtype = models.CharField(max_length=100)
    question = models.TextField(null=True)
    section = models.CharField(max_length=10, default='A')
    input_ans = models.TextField(default='Not Answered')
    #rish added image field
    input_ans_Image = models.ImageField(upload_to='input_ans_images/', null=True, blank=True) 
    correct_ans = models.TextField()
    marks = models.FloatField()
    check = models.CharField(max_length=100, default='Not Answered')
    level = models.CharField(max_length=100, default='medium')
    marks_given = models.FloatField(default=0)
    time = models.FloatField(default=0)
    extra_time = models.FloatField(default=0)
    negative_marks = models.FloatField()

    def __str__(self):
        return self.question
