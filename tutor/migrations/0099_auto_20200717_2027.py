# Generated by Django 3.0.5 on 2020-07-17 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutor', '0098_auto_20200717_2027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addstudentdetail',
            name='feeDisc',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, null=True),
        ),
    ]
