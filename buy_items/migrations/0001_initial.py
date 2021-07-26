# Generated by Django 3.1.3 on 2021-07-15 09:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('notes', '0001_initial'),
        ('tutorials', '0001_initial'),
        ('exams', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Revenue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('price', models.FloatField(default=0)),
                ('product', models.CharField(max_length=100)),
                ('category', models.CharField(max_length=100)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer', to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owner', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BuyTutorTutorial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=0, null=True)),
                ('buy_at', models.DateField(auto_now_add=True)),
                ('order_id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('student', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.student')),
                ('tutorial', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tutorials.tutorialtutors')),
            ],
            options={
                'unique_together': {('tutorial', 'student')},
            },
        ),
        migrations.CreateModel(
            name='BuyTutorNotes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=0, null=True)),
                ('buy_at', models.DateField(auto_now_add=True)),
                ('order_id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('note', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='notes.notestutor')),
                ('student', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.student')),
            ],
            options={
                'unique_together': {('note', 'student')},
            },
        ),
        migrations.CreateModel(
            name='BuyTutorExam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=0, null=True)),
                ('buy_at', models.DateField(auto_now_add=True)),
                ('order_id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('exam', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='exams.tutorexam')),
                ('student', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.student')),
            ],
            options={
                'unique_together': {('student', 'exam')},
            },
        ),
        migrations.CreateModel(
            name='BuyInstituteTutorial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=0, null=True)),
                ('buy_at', models.DateField(auto_now_add=True)),
                ('order_id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('student', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.student')),
                ('tutorial', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tutorials.tutorialinstitute')),
            ],
            options={
                'unique_together': {('tutorial', 'student')},
            },
        ),
        migrations.CreateModel(
            name='BuyInstituteNotes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=0, null=True)),
                ('buy_at', models.DateField(auto_now_add=True)),
                ('order_id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('note', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='notes.notesinstitute')),
                ('student', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.student')),
            ],
            options={
                'unique_together': {('note', 'student')},
            },
        ),
    ]
