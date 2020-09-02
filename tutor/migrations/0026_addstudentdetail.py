# Generated by Django 3.0.5 on 2020-05-27 10:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tutor', '0025_delete_addstudentdetail'),
    ]

    operations = [
        migrations.CreateModel(
            name='AddStudentDetail',
            fields=[
                ('snum', models.AutoField(primary_key=True, serialize=False)),
                ('courseName', models.CharField(default='', max_length=255)),
                ('teachType', models.CharField(default='', max_length=255)),
                ('forclass', models.CharField(default='', max_length=255)),
                ('batch', models.CharField(default='', max_length=255)),
                ('username', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='AddStudentDetail', related_query_name='AddStudentDetail', to='tutor.AddStudentInst')),
            ],
        ),
    ]
