# Generated by Django 3.0.5 on 2020-06-01 18:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tutor', '0033_addstudentdetail_instalment'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubmitFees',
            fields=[
                ('sno', models.AutoField(primary_key=True, serialize=False)),
                ('totalFee', models.DecimalField(decimal_places=2, max_digits=10)),
                ('feePayed', models.DecimalField(decimal_places=2, max_digits=10)),
                ('balanceFee', models.DecimalField(decimal_places=2, max_digits=10)),
                ('instalmentDue', models.DecimalField(decimal_places=2, max_digits=10)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fees', to='tutor.TeachingType')),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fees', to='tutor.AddStudentDetail')),
            ],
        ),
        migrations.CreateModel(
            name='Instalment',
            fields=[
                ('sno', models.AutoField(primary_key=True, serialize=False)),
                ('instalmentNum', models.DecimalField(decimal_places=0, max_digits=3)),
                ('paymentExp', models.DecimalField(decimal_places=2, max_digits=10)),
                ('paymentDone', models.DecimalField(decimal_places=2, max_digits=10)),
                ('timeStamp', models.DateTimeField(auto_now_add=True)),
                ('feeObj', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Instalment', to='tutor.SubmitFees')),
            ],
        ),
    ]
