# Generated by Django 3.1.3 on 2021-04-15 08:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Class', models.CharField(max_length=20)),
                ('Batch', models.CharField(max_length=100)),
                ('Name', models.CharField(max_length=200)),
                ('exam_date', models.DateField()),
                ('exam_time', models.TimeField(blank=True, null=True)),
                ('exam_duration', models.IntegerField(default=0)),
                ('timezone', models.CharField(max_length=200)),
                ('pass_percentage', models.IntegerField()),
                ('reexam_date', models.DateField(blank=True, null=True)),
                ('calculator', models.BooleanField(default=False)),
                ('imgupload', models.BooleanField(default=False)),
                ('negative_marking', models.BooleanField(blank=True, default=False, null=True)),
                ('negative_marks', models.FloatField(blank=True, null=True)),
                ('tandc', models.TextField()),
                ('status', models.BooleanField(default=False)),
                ('resultonmail', models.BooleanField(blank=True, default=False, null=True)),
                ('question_count', models.IntegerField(default=0)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exams', to='courses.courses')),
                ('institute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='centername', to='accounts.institute')),
            ],
        ),
        migrations.CreateModel(
            name='TutorExam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('courseName', models.CharField(default='', max_length=100)),
                ('forclass', models.CharField(default='', max_length=255)),
                ('Name', models.CharField(max_length=200)),
                ('price', models.IntegerField()),
                ('exam_date', models.DateField()),
                ('exam_time', models.TimeField(blank=True, null=True)),
                ('exam_duration', models.IntegerField(default=0)),
                ('timezone', models.CharField(max_length=200)),
                ('pass_percentage', models.IntegerField()),
                ('reexam_date', models.DateField(blank=True, null=True)),
                ('calculator', models.BooleanField(default=False)),
                ('imgupload', models.BooleanField(default=False)),
                ('negative_marking', models.BooleanField(blank=True, default=False, null=True)),
                ('negative_marks', models.FloatField(blank=True, null=True)),
                ('tandc', models.TextField()),
                ('status', models.BooleanField(default=False)),
                ('resultonmail', models.BooleanField(blank=True, default=False, null=True)),
                ('question_count', models.IntegerField(default=0)),
                ('tutor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teacher', to='accounts.teacher')),
            ],
        ),
        migrations.CreateModel(
            name='TutorStudentMapping',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('courseName', models.CharField(default='', max_length=100)),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_exam', to='exams.tutorexam')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_tutor_mapping', to='accounts.student')),
            ],
        ),
        migrations.CreateModel(
            name='TutorStudentExamResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marks_scored', models.FloatField(default=0)),
                ('total_marks', models.FloatField(default=0)),
                ('total_questions', models.IntegerField(default=0)),
                ('attempted', models.BooleanField(default=False)),
                ('percentage', models.CharField(default='10', max_length=10)),
                ('pass_status', models.BooleanField(default=False)),
                ('time_taken', models.CharField(default=0, max_length=100)),
                ('annotated_copies', models.FileField(blank=True, null=True, upload_to='annotated_pdf')),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exams.tutorexam')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exams.tutorstudentmapping')),
            ],
        ),
        migrations.CreateModel(
            name='TutorStudentAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qtype', models.CharField(max_length=100)),
                ('question', models.TextField(null=True)),
                ('section', models.CharField(default='A', max_length=10)),
                ('input_ans', models.TextField(default='Not Answered')),
                ('input_ans_Image', models.ImageField(blank=True, null=True, upload_to='input_ans_images/')),
                ('correct_ans', models.TextField()),
                ('marks', models.FloatField()),
                ('check', models.CharField(default='Not Answered', max_length=100)),
                ('level', models.CharField(default='medium', max_length=100)),
                ('marks_given', models.FloatField(default=0)),
                ('time', models.FloatField(default=0)),
                ('extra_time', models.FloatField(default=0)),
                ('negative_marks', models.FloatField()),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exams.tutorexam')),
                ('student', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='exams.tutorstudentmapping')),
            ],
        ),
        migrations.CreateModel(
            name='TutorMultipleQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField()),
                ('correct_ans', models.CharField(max_length=1000)),
                ('marks', models.FloatField()),
                ('question_no', models.IntegerField(default=0)),
                ('level', models.CharField(default='medium', max_length=100)),
                ('negative_marks', models.FloatField(default=0)),
                ('section', models.CharField(default='A', max_length=10)),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='multiple_question', to='exams.tutorexam')),
            ],
            options={
                'unique_together': {('exam', 'question')},
            },
        ),
        migrations.CreateModel(
            name='TutorMultipleAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('option', models.CharField(max_length=150)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='options', to='exams.tutormultiplequestion')),
            ],
        ),
        migrations.CreateModel(
            name='StudentMapping',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_course', to='courses.courses')),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_exam', to='exams.exam')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_mapping', to='accounts.student')),
            ],
        ),
        migrations.CreateModel(
            name='StudentExamResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marks_scored', models.FloatField(default=0)),
                ('total_marks', models.FloatField(default=0)),
                ('total_questions', models.IntegerField(default=0)),
                ('attempted', models.BooleanField(default=False)),
                ('percentage', models.CharField(default='10', max_length=10)),
                ('pass_status', models.BooleanField(default=False)),
                ('time_taken', models.CharField(default=0, max_length=100)),
                ('annotated_copies', models.FileField(blank=True, null=True, upload_to='annotated_pdf')),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exams.exam')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exams.studentmapping')),
            ],
        ),
        migrations.CreateModel(
            name='StudentAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qtype', models.CharField(max_length=100)),
                ('question', models.TextField(null=True)),
                ('section', models.CharField(default='A', max_length=10)),
                ('input_ans', models.TextField(default='Not Answered')),
                ('input_ans_Image', models.ImageField(blank=True, null=True, upload_to='input_ans_images/')),
                ('correct_ans', models.TextField()),
                ('marks', models.FloatField()),
                ('check', models.CharField(default='Not Answered', max_length=100)),
                ('level', models.CharField(default='medium', max_length=100)),
                ('marks_given', models.FloatField(default=0)),
                ('time', models.FloatField(default=0)),
                ('extra_time', models.FloatField(default=0)),
                ('negative_marks', models.FloatField()),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exams.exam')),
                ('student', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='exams.studentmapping')),
            ],
        ),
        migrations.CreateModel(
            name='MultipleQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField()),
                ('correct_ans', models.CharField(max_length=1000)),
                ('marks', models.FloatField()),
                ('question_no', models.IntegerField(default=0)),
                ('level', models.CharField(default='medium', max_length=100)),
                ('negative_marks', models.FloatField(default=0)),
                ('section', models.CharField(default='A', max_length=10)),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='multiple_question', to='exams.exam')),
            ],
            options={
                'unique_together': {('exam', 'question')},
            },
        ),
        migrations.CreateModel(
            name='MultipleAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('option', models.CharField(max_length=150)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='options', to='exams.multiplequestion')),
            ],
        ),
        migrations.CreateModel(
            name='TutorShortAnswerQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField()),
                ('correct_ans', models.TextField(max_length=150)),
                ('marks', models.FloatField()),
                ('question_no', models.IntegerField(default=0)),
                ('level', models.CharField(default='medium', max_length=100)),
                ('negative_marks', models.FloatField()),
                ('section', models.CharField(max_length=10)),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='oneline_question', to='exams.tutorexam')),
            ],
            options={
                'unique_together': {('exam', 'question')},
            },
        ),
        migrations.CreateModel(
            name='TutorLongAnswerQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField()),
                ('level', models.CharField(default='medium', max_length=100)),
                ('correct_ans', models.TextField(max_length=350)),
                ('marks', models.FloatField()),
                ('question_no', models.IntegerField(default=0)),
                ('negative_marks', models.FloatField()),
                ('section', models.CharField(max_length=10)),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subjective_question', to='exams.tutorexam')),
            ],
            options={
                'unique_together': {('exam', 'question')},
            },
        ),
        migrations.CreateModel(
            name='TutorBooleanQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField()),
                ('option1', models.CharField(blank=True, max_length=1000, null=True)),
                ('option2', models.CharField(blank=True, max_length=1000, null=True)),
                ('correct_ans', models.CharField(max_length=1000)),
                ('marks', models.FloatField()),
                ('question_no', models.IntegerField(default=0)),
                ('level', models.CharField(default='medium', max_length=100)),
                ('negative_marks', models.FloatField()),
                ('section', models.CharField(max_length=10)),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='boolean_question', to='exams.tutorexam')),
            ],
            options={
                'unique_together': {('exam', 'question')},
            },
        ),
        migrations.CreateModel(
            name='ShortAnswerQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField()),
                ('correct_ans', models.TextField(max_length=150)),
                ('marks', models.FloatField()),
                ('question_no', models.IntegerField(default=0)),
                ('level', models.CharField(default='medium', max_length=100)),
                ('negative_marks', models.FloatField()),
                ('section', models.CharField(max_length=10)),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='oneline_question', to='exams.exam')),
            ],
            options={
                'unique_together': {('exam', 'question')},
            },
        ),
        migrations.CreateModel(
            name='LongAnswerQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField()),
                ('level', models.CharField(default='medium', max_length=100)),
                ('correct_ans', models.TextField(max_length=350)),
                ('marks', models.FloatField()),
                ('question_no', models.IntegerField(default=0)),
                ('negative_marks', models.FloatField()),
                ('section', models.CharField(max_length=10)),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subjective_question', to='exams.exam')),
            ],
            options={
                'unique_together': {('exam', 'question')},
            },
        ),
        migrations.CreateModel(
            name='BooleanQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField()),
                ('option1', models.CharField(blank=True, max_length=1000, null=True)),
                ('option2', models.CharField(blank=True, max_length=1000, null=True)),
                ('correct_ans', models.CharField(max_length=1000)),
                ('marks', models.FloatField()),
                ('question_no', models.IntegerField(default=0)),
                ('level', models.CharField(default='medium', max_length=100)),
                ('negative_marks', models.FloatField()),
                ('section', models.CharField(max_length=10)),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='boolean_question', to='exams.exam')),
            ],
            options={
                'unique_together': {('exam', 'question')},
            },
        ),
    ]
