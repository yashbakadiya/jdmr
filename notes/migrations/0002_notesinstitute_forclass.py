# Generated by Django 3.0.5 on 2021-03-01 03:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='notesinstitute',
            name='forclass',
            field=models.CharField(default='', max_length=150),
        ),
    ]