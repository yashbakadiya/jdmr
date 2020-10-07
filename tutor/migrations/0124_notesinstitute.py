# Generated by Django 3.1b1 on 2020-10-02 17:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tutor', '0123_auto_20200921_2252'),
    ]

    operations = [
        migrations.CreateModel(
            name='NotesInstitute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notes', models.FileField(upload_to='notes/Institute')),
                ('title', models.CharField(max_length=2000)),
                ('subject', models.CharField(max_length=3000)),
                ('center', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='centernotes', to='tutor.signupcoachingcentre')),
            ],
        ),
    ]