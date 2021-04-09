# Generated by Django 3.1.3 on 2021-04-09 04:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Courses',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('courseID', models.CharField(default='', max_length=25)),
                ('courseName', models.CharField(default='', max_length=100)),
                ('forclass', models.CharField(default='', max_length=150)),
                ('archieved', models.BooleanField(default=False)),
                ('intitute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='AddCourses', to='accounts.institute')),
            ],
        ),
        migrations.CreateModel(
            name='TeachingType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('courseID', models.IntegerField(default=None)),
                ('forclass', models.CharField(default='', max_length=255)),
                ('teachType', models.CharField(default='', max_length=255)),
                ('duration', models.CharField(default='', max_length=255)),
                ('timePeriod', models.CharField(default='', max_length=255)),
                ('archieved', models.BooleanField(default=False)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='TeachingType', to='courses.courses')),
            ],
        ),
    ]
