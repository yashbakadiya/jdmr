from django.contrib import admin
from .models import Enquiry, Course, EmailInfo, GetContent, Register, Transaction, Pdf, Voucher, Instructor, Category, SubCategory, Tag, Syllabus, Language
from import_export.admin import ImportExportModelAdmin
from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter
# Register your models here.


# @admin.register(Enquiry)
# class EnquiryAdmin(ImportExportModelAdmin):
#     list_display = ('id', 'full_name', 'email', 'phone_num',
#                     'course', 'message', 'created_at')
#     list_filter = (('created_at', DateRangeFilter), 'course',)
#     pass


# @admin.register(Instructor)
# class InstructorAdmin(admin.ModelAdmin):
#     list_display = ('id', 'instructor_name',
#                     'instructor_edu', 'instructor_desc')


# @admin.register(Tag)
# class TagAdmin(admin.ModelAdmin):
#     list_display = ('id', 'tag_name')


# @admin.register(Category)
# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ('id', 'category_name', 'available')


# @admin.register(SubCategory)
# class SubCategoryAdmin(admin.ModelAdmin):
#     list_display = ('id', 'sub_category_name', 'available')


# @admin.register(Syllabus)
# class SyllabusAdmin(admin.ModelAdmin):
#     list_display = ('id', 'syllabus')


# @admin.register(Language)
# class LanguageAdmin(admin.ModelAdmin):
#     list_display = ('id', 'language')


# @admin.register(Register)
# class RegisterAdmin(ImportExportModelAdmin):
#     list_display = ('id', 'registerid', 'full_name', 'email', 'phone_num', 'college_name',
#                     'course', 'amount', 'created_at')
#     list_filter = (('created_at', DateRangeFilter), 'course',)
#     pass


# @admin.register(Course)
# class CourseAdmin(admin.ModelAdmin):
#     readonly_fields = ('discounted_price', 'course_timing')
#     list_display = ('id', 'course_name', 'category', 'course_language', 'course_timing',
#                     'actual_price', 'discount_percentage', 'discount_rs', 'discounted_price', 'available', 'course_start_date')
#     pass


# @admin.register(EmailInfo)
# class EmailInfoAdmin(admin.ModelAdmin):
#     list_display = ('id', 'subject', 'body', 'attachment')
#     pass


# @admin.register(GetContent)
# class GetContentAdmin(ImportExportModelAdmin):
#     list_display = ('id', 'full_name', 'email', 'phone_num', 'created_at')
#     list_filter = (('created_at', DateRangeFilter),)
#     pass


# @admin.register(Transaction)
# class TransactionAdmin(ImportExportModelAdmin):
#     list_display = ('id', 'orderid', 'currency', 'gatewayname',
#                     'respmsg', 'bankname', 'paymentmode', 'mid',
#                     'respcode', 'txnid', 'txnamount', 'status', 'banktxnid', 'txndate')
#     pass


# @admin.register(Pdf)
# class PdfAdmin(admin.ModelAdmin):
#     list_display = ('id', 'privacy_policy', 'terms_condition')
#     pass


# @admin.register(Voucher)
# class VoucherAdmin(admin.ModelAdmin):
#     list_display = ('id', 'coupen_code', 'validity', 'amount')
#     pass
