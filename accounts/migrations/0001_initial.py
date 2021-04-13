# Generated by Django 3.1.3 on 2021-04-13 07:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Tutorid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('teacherid', models.IntegerField(default='0')),
                ('teachername', models.CharField(default='None', max_length=100)),
                ('panaadhar', models.CharField(default='None', max_length=6)),
                ('panaadharnumber', models.CharField(default='None', max_length=18)),
                ('photoid', models.ImageField(blank=True, null=True, upload_to='photoID/')),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(default='1234567899', max_length=10)),
                ('address', models.CharField(blank=True, max_length=200)),
                ('photo', models.ImageField(blank=True, default='default-man.png', null=True, upload_to='users/')),
                ('emailValidated', models.BooleanField(blank=True, default=False)),
                ('phoneValidated', models.BooleanField(blank=True, default=False)),
                ('pincode', models.CharField(default='000000', max_length=6)),
                ('dob', models.DateField(blank=True, default='2020-12-1')),
                ('gender', models.CharField(default='Male', max_length=6)),
                ('forclass', models.CharField(default='None', max_length=30)),
                ('desc', models.TextField(default='None')),
                ('course', models.CharField(default='None', max_length=150)),
                ('qualification', models.CharField(default='None', max_length=100)),
                ('experiance', models.IntegerField(default=-1)),
                ('fees', models.IntegerField(default=1000)),
                ('democlass', models.BooleanField(default=False)),
                ('availability', models.CharField(default='None', max_length=30)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(default='1234567899', max_length=10)),
                ('address', models.CharField(blank=True, max_length=200)),
                ('photo', models.ImageField(blank=True, default='default-man.png', null=True, upload_to='users/')),
                ('emailValidated', models.BooleanField(blank=True, default=False)),
                ('phoneValidated', models.BooleanField(blank=True, default=False)),
                ('pincode', models.CharField(default='000000', max_length=6)),
                ('schoolName', models.CharField(default=' ', max_length=150)),
                ('dob', models.DateField(blank=True, default='2020-12-1')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Institute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(default='1234567899', max_length=10)),
                ('address', models.CharField(blank=True, max_length=200)),
                ('photo', models.ImageField(blank=True, default='default-man.png', null=True, upload_to='users/')),
                ('emailValidated', models.BooleanField(blank=True, default=False)),
                ('phoneValidated', models.BooleanField(blank=True, default=False)),
                ('pincode', models.CharField(default='000000', max_length=6)),
                ('latitude', models.CharField(default='0', max_length=20)),
                ('longitude', models.CharField(default='0', max_length=20)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
