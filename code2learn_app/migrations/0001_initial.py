# Generated by Django 3.1.3 on 2021-04-04 16:46

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=127)),
                ('available', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name_plural': 'categories',
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_name', models.CharField(max_length=80)),
                ('actual_price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('discount_rs', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=8)),
                ('discount_percentage', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=4, null=True)),
                ('discounted_price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('sub_heading', models.CharField(blank=True, max_length=255, null=True)),
                ('available', models.BooleanField()),
                ('course_start_date', models.DateField(blank=True, default=None, null=True)),
                ('course_start_time', models.TimeField(blank=True, default=None, null=True)),
                ('course_end_time', models.TimeField(blank=True, default=None, null=True)),
                ('course_timing', models.CharField(blank=True, max_length=63)),
                ('course_enrollment_end_date', models.DateField(blank=True, default=None, null=True)),
                ('prerequisites', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(upload_to='courses/thumbnails')),
                ('content', ckeditor.fields.RichTextField()),
                ('banner', models.ImageField(upload_to='courses/banners')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='code2learn_app.category')),
            ],
        ),
        migrations.CreateModel(
            name='EmailInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=200)),
                ('body', models.TextField()),
                ('attachment', models.FileField(upload_to='pdf')),
            ],
        ),
        migrations.CreateModel(
            name='Enquiry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=80)),
                ('email', models.EmailField(max_length=254)),
                ('phone_num', models.CharField(max_length=15)),
                ('course', models.CharField(max_length=80, null=True)),
                ('message', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'enquiries',
            },
        ),
        migrations.CreateModel(
            name='GetContent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=80)),
                ('email', models.EmailField(max_length=254)),
                ('phone_num', models.CharField(max_length=15)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Instructor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('instructor_name', models.CharField(max_length=80)),
                ('instructor_edu', models.CharField(max_length=255)),
                ('instructor_desc', models.TextField()),
                ('instructor_image', models.ImageField(upload_to='instructors')),
            ],
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(default='English', max_length=63)),
            ],
        ),
        migrations.CreateModel(
            name='Pdf',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('privacy_policy', models.FileField(upload_to='pdf')),
                ('terms_condition', models.FileField(upload_to='pdf')),
            ],
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub_category_name', models.CharField(max_length=127)),
                ('available', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name_plural': 'subcategories',
            },
        ),
        migrations.CreateModel(
            name='Syllabus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('syllabus', models.FileField(null=True, upload_to='syllabus')),
            ],
            options={
                'verbose_name_plural': 'syllabi',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_name', models.CharField(max_length=63)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('orderid', models.CharField(max_length=80)),
                ('currency', models.CharField(max_length=50)),
                ('gatewayname', models.CharField(max_length=200)),
                ('respmsg', models.TextField()),
                ('bankname', models.CharField(max_length=100)),
                ('paymentmode', models.CharField(max_length=100)),
                ('mid', models.CharField(max_length=100)),
                ('respcode', models.CharField(max_length=50)),
                ('txnid', models.CharField(max_length=200)),
                ('txnamount', models.CharField(max_length=50)),
                ('status', models.CharField(max_length=80)),
                ('banktxnid', models.CharField(max_length=100)),
                ('txndate', models.CharField(max_length=80)),
            ],
        ),
        migrations.CreateModel(
            name='Voucher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coupen_code', models.CharField(max_length=20)),
                ('validity', models.DateField()),
                ('amount', models.DecimalField(decimal_places=2, max_digits=8)),
            ],
        ),
        migrations.CreateModel(
            name='Register',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('registerid', models.CharField(max_length=80)),
                ('full_name', models.CharField(max_length=80)),
                ('email', models.EmailField(max_length=254)),
                ('phone_num', models.CharField(max_length=15)),
                ('college_name', models.CharField(max_length=80)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=8)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='code2learn_app.course')),
                ('voucher', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='code2learn_app.voucher')),
            ],
        ),
        migrations.AddField(
            model_name='course',
            name='course_language',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='code2learn_app.language'),
        ),
        migrations.AddField(
            model_name='course',
            name='instructor_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='code2learn_app.instructor'),
        ),
        migrations.AddField(
            model_name='course',
            name='sub_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='code2learn_app.subcategory'),
        ),
        migrations.AddField(
            model_name='course',
            name='syllabus',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, to='code2learn_app.syllabus'),
        ),
        migrations.AddField(
            model_name='course',
            name='tag_name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='code2learn_app.tag'),
        ),
    ]
