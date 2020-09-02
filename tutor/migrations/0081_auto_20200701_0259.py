# Generated by Django 3.0.5 on 2020-06-30 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutor', '0080_auto_20200630_0024'),
    ]

    operations = [
        migrations.AddField(
            model_name='signupcoachingcentre',
            name='latitude',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=5),
        ),
        migrations.AddField(
            model_name='signupcoachingcentre',
            name='longitude',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=5),
        ),
        migrations.AddField(
            model_name='signupstudent',
            name='latitude',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=5),
        ),
        migrations.AddField(
            model_name='signupstudent',
            name='longitude',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=5),
        ),
        migrations.AddField(
            model_name='signuptutor',
            name='latitude',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=5),
        ),
        migrations.AddField(
            model_name='signuptutor',
            name='longitude',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=5),
        ),
    ]
