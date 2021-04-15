# Generated by Django 3.1.3 on 2021-04-15 08:02

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NotesTutor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notes', models.FileField(upload_to='notes/Institute')),
                ('title', models.CharField(max_length=2000)),
                ('subject', models.CharField(max_length=3000)),
                ('forclass', models.CharField(default='', max_length=150)),
                ('description', models.TextField(max_length=150)),
                ('price', models.IntegerField(default=0)),
                ('date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('tutor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tutornotes', to='accounts.teacher')),
            ],
        ),
        migrations.CreateModel(
            name='NotesInstitute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notes', models.FileField(upload_to='notes/Institute')),
                ('title', models.CharField(max_length=2000)),
                ('subject', models.CharField(max_length=3000)),
                ('forclass', models.CharField(default='', max_length=150)),
                ('description', models.TextField(max_length=150)),
                ('price', models.IntegerField(default=0)),
                ('freeEnrolled', models.BooleanField(default=False)),
                ('date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('institute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='centernotes', to='accounts.institute')),
            ],
        ),
    ]
