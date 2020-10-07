# Generated by Django 3.1b1 on 2020-09-17 13:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tutor', '0121_auto_20200914_2044'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentMapping',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_course', to='tutor.addcourses')),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_exam', to='tutor.exam')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_mapping', to='tutor.signupstudent')),
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
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tutor.exam')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tutor.studentmapping')),
            ],
        ),
        migrations.CreateModel(
            name='StudentAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qtype', models.CharField(max_length=100)),
                ('question', models.TextField()),
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
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tutor.exam')),
                ('student', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tutor.studentmapping')),
            ],
        ),
    ]