# Generated by Django 3.0.5 on 2020-06-10 10:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tutor', '0047_archivestudents'),
    ]

    operations = [
        migrations.CreateModel(
            name='tutorInstitute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inst', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tutorInstitute', to='tutor.SignupCoachingCentre')),
                ('tutor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tutorInstitute', to='tutor.enrollTutors')),
            ],
        ),
    ]
