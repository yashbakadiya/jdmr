# Generated by Django 3.1.3 on 2021-04-04 16:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ChatApplication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dtime', models.DateTimeField(default=datetime.datetime.now)),
                ('message', models.CharField(max_length=60)),
                ('names', models.CharField(default='Welcome', max_length=60)),
                ('room', models.CharField(max_length=30)),
                ('fl', models.IntegerField()),
                ('ts', models.CharField(max_length=30)),
                ('chatroom', models.CharField(default='Welcome', max_length=30)),
            ],
        ),
    ]
