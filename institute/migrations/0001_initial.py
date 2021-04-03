# Generated by Django 3.0.5 on 2021-02-09 09:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='InstituteRatings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Posted_On', models.DateField(auto_now_add=True)),
                ('Review', models.TextField()),
                ('Rating', models.PositiveIntegerField()),
                ('institute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Coachingreviews', to='accounts.Institute')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='studentenrolledinstitute', to='accounts.Student')),
            ],
            options={
                'ordering': ['-Posted_On'],
            },
        ),
    ]
