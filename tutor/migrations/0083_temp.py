# Generated by Django 3.0.5 on 2020-07-03 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutor', '0082_auto_20200701_2117'),
    ]

    operations = [
        migrations.CreateModel(
            name='temp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recc', models.BooleanField()),
            ],
        ),
    ]
