# Generated by Django 3.0.1 on 2020-04-24 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutor', '0014_auto_20200424_2028'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addtutorinst',
            name='instituteCode',
            field=models.CharField(default='', max_length=255),
        ),
    ]
