# Generated by Django 3.0.5 on 2020-05-25 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutor', '0020_auto_20200518_1113'),
    ]

    operations = [
        migrations.CreateModel(
            name='AddFeesC',
            fields=[
                ('sno', models.AutoField(primary_key=True, serialize=False)),
                ('courseName', models.CharField(default='', max_length=100)),
                ('forclass', models.CharField(default='', max_length=255)),
                ('teachType', models.CharField(default='', max_length=255)),
                ('duration', models.CharField(default='', max_length=255)),
                ('fee_amt', models.CharField(default='', max_length=100)),
                ('tax', models.CharField(default='', max_length=100)),
                ('final_amt', models.CharField(default='', max_length=100)),
                ('no_of_installment', models.CharField(default='', max_length=100)),
                ('extra_charge', models.CharField(default='', max_length=255)),
            ],
        ),
    ]
