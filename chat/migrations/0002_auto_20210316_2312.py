# Generated by Django 3.0.5 on 2021-03-16 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatapplication',
            name='names',
            field=models.CharField(default='user', max_length=60),
        ),
        migrations.AlterField(
            model_name='chatapplication',
            name='fl',
            field=models.IntegerField(max_length=2),
        ),
    ]
