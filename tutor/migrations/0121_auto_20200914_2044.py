# Generated by Django 3.1b1 on 2020-09-14 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutor', '0120_auto_20200913_1524'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booleanquestion',
            name='correct_ans',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='booleanquestion',
            name='option1',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='booleanquestion',
            name='option2',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]