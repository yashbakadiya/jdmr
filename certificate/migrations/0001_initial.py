# Generated by Django 3.0.5 on 2021-03-31 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Certificate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('certificate_num', models.CharField(max_length=30)),
                ('register_num', models.CharField(max_length=30)),
                ('issued', models.BooleanField(default=False)),
                ('issued_date', models.DateField(blank=True, default=None, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Certificate_sign',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sign', models.ImageField(upload_to='sign')),
            ],
        ),
        migrations.CreateModel(
            name='Qrcode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('certificate_num', models.CharField(max_length=30)),
                ('name', models.CharField(max_length=30)),
                ('link', models.CharField(max_length=200)),
                ('qr_code', models.ImageField(blank=True, upload_to='qr_codes')),
            ],
        ),
    ]
