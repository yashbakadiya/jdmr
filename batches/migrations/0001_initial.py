# Generated by Django 3.1.3 on 2021-04-20 08:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BatchTiming',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('batchName', models.CharField(default='', max_length=255, unique=True)),
                ('days', models.CharField(default='', help_text='Comma seperated', max_length=255)),
                ('startTime', models.CharField(default='', max_length=255)),
                ('endTime', models.CharField(default='', max_length=255)),
                ('original24time', models.CharField(default='', help_text='Comma seperated', max_length=255)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('course', models.CharField(default='', max_length=150)),
                ('forclass', models.CharField(default='', max_length=150)),
                ('teachingtype', models.CharField(default='', max_length=150)),
                ('institute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='BatchTiming', to='accounts.institute')),
            ],
        ),
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=35)),
                ('description', models.TextField()),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('batch', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Notice', to='batches.batchtiming')),
            ],
        ),
        migrations.CreateModel(
            name='BatchTimingTutor',
            fields=[
                ('sno', models.AutoField(primary_key=True, serialize=False)),
                ('batchName', models.CharField(default='', max_length=255)),
                ('days', models.CharField(default='', help_text='Comma seperated', max_length=255)),
                ('startTime', models.CharField(default='', max_length=255)),
                ('endTime', models.CharField(default='', max_length=255)),
                ('original24time', models.CharField(default='', help_text='Comma seperated', max_length=255)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('StartDate', models.DateTimeField()),
                ('EndDate', models.DateTimeField()),
                ('Tutor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='BatchTutor', to='accounts.teacher')),
            ],
        ),
    ]
