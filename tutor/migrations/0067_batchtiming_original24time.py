# Generated by Django 3.0.5 on 2020-06-19 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutor', '0066_auto_20200619_1600'),
    ]

    operations = [
        migrations.AddField(
            model_name='batchtiming',
            name='original24time',
            field=models.CharField(default='', help_text='Comma seperated', max_length=255),
        ),
    ]
