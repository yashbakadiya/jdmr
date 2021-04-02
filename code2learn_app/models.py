from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.


class Enquiry(models.Model):
    full_name = models.CharField(max_length=80)
    email = models.EmailField(max_length=254)
    phone_num = models.CharField(max_length=15)
    course = models.CharField(max_length=80, null=True)
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "enquiries"


class Instructor(models.Model):
    instructor_name = models.CharField(max_length=80)
    instructor_edu = models.CharField(max_length=255)
    instructor_desc = models.TextField()
    instructor_image = models.ImageField(upload_to="instructors")

    def __str__(self) -> str:
        return f'{self.instructor_name}'


class Category(models.Model):
    category_name = models.CharField(max_length=127)
    available = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self) -> str:
        return f'{self.category_name}'


class SubCategory(models.Model):
    sub_category_name = models.CharField(max_length=127)
    available = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "subcategories"

    def __str__(self) -> str:
        return f'{self.sub_category_name}'


class Tag(models.Model):
    tag_name = models.CharField(max_length=63)

    def __str__(self) -> str:
        return f'{self.tag_name}'


class Language(models.Model):
    language = models.CharField(max_length=63, default='English')

    def __str__(self) -> str:
        return f'{self.language}'


class Syllabus(models.Model):
    syllabus = models.FileField(
        upload_to="syllabus", null=True)

    class Meta:
        verbose_name_plural = 'syllabi'

    def __str__(self) -> str:
        return f'{self.syllabus}'


class Voucher(models.Model):
    coupen_code = models.CharField(max_length=20)
    validity = models.DateField()
    amount = models.DecimalField(max_digits=8, decimal_places=2)


class Course(models.Model):
    tag_name = models.ForeignKey(Tag, on_delete=models.PROTECT, null=True)
    course_name = models.CharField(max_length=80)
    course_language = models.ForeignKey(Language, on_delete=models.PROTECT)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.PROTECT)
    actual_price = models.DecimalField(max_digits=8, decimal_places=2)
    discount_rs = models.DecimalField(
        max_digits=8, decimal_places=2, blank=True, default=0)
    discount_percentage = models.DecimalField(
        max_digits=4, decimal_places=2, blank=True, null=True, default=0)
    discounted_price = models.DecimalField(max_digits=8, decimal_places=2)
    sub_heading = models.CharField(max_length=255, null=True, blank=True)
    available = models.BooleanField()
    course_start_date = models.DateField(default=None, null=True, blank=True)
    course_start_time = models.TimeField(default=None, blank=True, null=True)
    course_end_time = models.TimeField(default=None, blank=True, null=True)
    course_timing = models.CharField(max_length=63, blank=True)
    course_enrollment_end_date = models.DateField(
        default=None, null=True, blank=True)
    prerequisites = models.TextField(null=True, blank=True)
    instructor_name = models.ForeignKey(Instructor, on_delete=models.PROTECT)
    image = models.ImageField(upload_to="courses/thumbnails")
    syllabus = models.ForeignKey(
        Syllabus, on_delete=models.PROTECT, blank=True)
    content = RichTextField()
    banner = models.ImageField(upload_to="courses/banners")

    def save(self, *args, **kwargs):
        if self.discount_rs:
            self.discounted_price = self.actual_price - self.discount_rs
            self.discount_percentage = (self.discount_rs/self.actual_price)*100
        else:
            self.discount_rs = self.actual_price * self.discount_percentage / 100
            self.discounted_price = self.actual_price - self.discount_rs
        if self.course_start_time and self.course_end_time:
            self.course_timing = f'{self.course_start_time.strftime("%I:%M %p")} - {self.course_end_time.strftime("%I:%M %p")}'
        super(Course, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return f'{self.course_name}'


class Register(models.Model):
    registerid = models.CharField(max_length=80)
    full_name = models.CharField(max_length=80)
    email = models.EmailField(max_length=254)
    phone_num = models.CharField(max_length=15)
    college_name = models.CharField(max_length=80)
    course = models.ForeignKey(Course, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    voucher = models.ForeignKey(Voucher, on_delete=models.CASCADE, null=True)

class EmailInfo(models.Model):
    subject = models.CharField(max_length=200)
    body = models.TextField()
    attachment = models.FileField(
        upload_to="pdf")


class GetContent(models.Model):
    full_name = models.CharField(max_length=80)
    email = models.EmailField(max_length=254)
    phone_num = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)


class Transaction(models.Model):
    orderid = models.CharField(max_length=80)
    currency = models.CharField(max_length=50)
    gatewayname = models.CharField(max_length=200)
    respmsg = models.TextField()
    bankname = models.CharField(max_length=100)
    paymentmode = models.CharField(max_length=100)
    mid = models.CharField(max_length=100)
    respcode = models.CharField(max_length=50)
    txnid = models.CharField(max_length=200)
    txnamount = models.CharField(max_length=50)
    status = models.CharField(max_length=80)
    banktxnid = models.CharField(max_length=100)
    txndate = models.CharField(max_length=80)


class Pdf(models.Model):
    privacy_policy = models.FileField(
        upload_to="pdf")
    terms_condition = models.FileField(
        upload_to="pdf")
