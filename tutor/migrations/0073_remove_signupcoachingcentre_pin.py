# Generated by Django 3.0.5 on 2020-06-26 11:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tutor', '0072_signupcoachingcentre_location'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='signupcoachingcentre',
            name='pin',
        ),
    ]
