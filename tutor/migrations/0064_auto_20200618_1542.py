# Generated by Django 3.0.5 on 2020-06-18 10:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tutor', '0063_addtutorsinst_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addtutorsinst',
            name='username',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='AddTutorsInst', to='tutor.enrollTutors'),
        ),
    ]
