# Generated by Django 3.0.5 on 2020-07-10 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutor', '0088_auto_20200710_0118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='archivecourses',
            name='crclass',
            field=models.CharField(default='', max_length=150),
        ),
    ]
