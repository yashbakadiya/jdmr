from django.contrib.admin.decorators import register
from certificate.views import certificatenum
from django.contrib import admin
from .models import Qrcode, Certificate, Certificate_sign
from import_export.admin import ImportExportModelAdmin
from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter
# Register your models here.


# def make_issued(modeladmin, request, queryset):
#     for certificateobj in queryset:
#         certificateobj.issued = True
#         certificateobj.save()

#         certificate_num = certificateobj.certificate_num
#         register_num = certificateobj.register_num
#         print(certificate_num)
#         print(register_num)

#         qrlink = "https://code2learn.co/certificate/"+certificate_num
#         qrcodeobj = Qrcode(name=certificate_num, link=qrlink)
#         qrcodeobj.save()


# make_issued.short_description = "Issue Certificates"


# @admin.register(Qrcode)
# class QrcodeAdmin(ImportExportModelAdmin):
#     list_display = ('id', 'name', 'link', 'qr_code')

# @admin.register(Certificate_sign)
# class Certificate_signAdmin(ImportExportModelAdmin):
#     list_display = ('id', 'sign')


# @admin.register(Certificate)
# class CertificateAdmin(ImportExportModelAdmin):
#     list_display = ('id', 'certificate_num',
#                     'register_num', 'issued')
#     actions = [make_issued]
