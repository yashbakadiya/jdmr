# Generated by Django 3.0.5 on 2020-06-04 23:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutor', '0042_submitfees_totalinstallments'),
    ]

    operations = [
        migrations.AddField(
            model_name='submitfees',
            name='previousDebt',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
