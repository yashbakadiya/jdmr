# Generated by Django 3.0.5 on 2020-07-23 05:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tutor', '0103_auto_20200723_1030'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='addfeesc',
            name='discValidity',
        ),
    ]
