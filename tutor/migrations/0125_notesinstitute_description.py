# Generated by Django 3.1b1 on 2020-10-02 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutor', '0124_notesinstitute'),
    ]

    operations = [
        migrations.AddField(
            model_name='notesinstitute',
            name='description',
            field=models.TextField(default='default'),
            preserve_default=False,
        ),
    ]
