# Generated by Django 3.0.5 on 2021-02-09 09:28

from django.db import migrations, models
import django.db.models.deletion
import students.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='PostTution',
            fields=[
                ('sno', models.AutoField(primary_key=True, serialize=False)),
                ('subject', models.CharField(default='', max_length=255)),
                ('forclass', models.CharField(default='', max_length=255)),
                ('teachingMode', models.CharField(default='', max_length=255)),
                ('genderPreference', models.CharField(default='', help_text='Female/Male', max_length=10)),
                ('whenToStart', models.CharField(default='', max_length=255)),
                ('description', models.CharField(default='', max_length=1024)),
                ('budget', models.CharField(default='', help_text='Hourly/Monthly', max_length=10)),
                ('budgetVal', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('numberOfSessions', models.DecimalField(decimal_places=0, default=0, max_digits=4)),
                ('assigned', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('student', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='PostTution', to='accounts.Student')),
            ],
        ),
        migrations.CreateModel(
            name='PostAssignment',
            fields=[
                ('sno', models.AutoField(primary_key=True, serialize=False)),
                ('courseName', models.CharField(default='', max_length=255)),
                ('forclass', models.CharField(default='', max_length=255)),
                ('description', models.CharField(default='', max_length=1024)),
                ('descriptionFile', models.FileField(blank=True, null=True, upload_to=students.models.assignmentDescriptionFiles)),
                ('requirement', models.DecimalField(decimal_places=0, max_digits=4)),
                ('budget', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('assigned', models.BooleanField(default=False)),
                ('student', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='PostAssignment', to='accounts.Student')),
            ],
        ),
        migrations.CreateModel(
            name='AddStudentInst',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('courseName', models.CharField(default='', max_length=100)),
                ('forclass', models.CharField(default='', max_length=255)),
                ('teachType', models.CharField(default='', max_length=255)),
                ('batch', models.CharField(default='', max_length=30)),
                ('feeDisc', models.DecimalField(decimal_places=3, default=0, max_digits=10)),
                ('installments', models.IntegerField(default=2)),
                ('archieved', models.BooleanField(default=False)),
                ('institute', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='AddStudentInst', to='accounts.Institute')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Student')),
            ],
        ),
    ]
