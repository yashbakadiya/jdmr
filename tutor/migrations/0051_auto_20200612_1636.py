# Generated by Django 3.0.5 on 2020-06-12 11:06

from django.db import migrations, models
import tutor.models


class Migration(migrations.Migration):

    dependencies = [
        ('tutor', '0050_signuptutorcontinued'),
    ]

    operations = [
        migrations.AlterField(
            model_name='signuptutorcontinued',
            name='gender',
            field=models.CharField(default='', help_text='Female/Male', max_length=10),
        ),
        migrations.AlterField(
            model_name='signuptutorcontinued',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to=tutor.models.userImagePath),
        ),
    ]
