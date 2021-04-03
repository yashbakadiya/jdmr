import json
from django.http.response import Http404
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.http import JsonResponse
from datetime import date
import decimal
from django.db.models import Q
from .models import Enquiry, EmailInfo, GetContent, Register, Transaction, Pdf, Voucher, Category, Course
from certificate.models import Certificate, Qrcode
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from tutorSearch.settings import EMAIL_HOST_USER, MERCHANT_KEY, MID
from django.views.static import serve
from django.http import FileResponse
import hmac
import hashlib
from django.views.decorators.csrf import csrf_exempt
from .paytm import generate_checksum, verify_checksum
import razorpay
import string
import random
from users.models import User
from django.conf import settings
from django.db import IntegrityError
import re
from users.views import create_new_user, check_user
from code2learn_app.middlewares.auth import login_excluded


# For Paytm and Razorpay
KEY_ID = settings.KEY_ID
KEY_SECRET = settings.KEY_SECRET
MID = settings.MID
MERCHANT_KEY = settings.MERCHANT_KEY

def main(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    else:
        return redirect('home')

# Create your views here.
def index(request):
    categories = Category.objects.filter(available=True)
    context = {
        'categories': categories,
        'pdf': Pdf.objects.all().first()
    }
    for i in range(len(categories)):
        context[f'course_{i+1}'] = Course.objects.filter(
            available=True, category=categories[i]).order_by('-id')

    if request.method == "POST":

        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        phonenum = request.POST.get('phonenum')

        enquiry = Enquiry(full_name=fullname, email=email,
                          phone_num=phonenum)
        enquiry.save()

        # email1 = EmailInfo.objects.get(id=1)
        data = {
            'receiver': fullname.split(" ")[0].capitalize()
        }

        html_content = render_to_string("emails/enquiry.html", data)
        text_content = strip_tags(html_content)

        email = EmailMultiAlternatives(
            f"Enquiry Form Submission",
            text_content,
            "Code2Learn <contact@code2learn.co>",
            [email]
        )
        email.attach_alternative(html_content, "text/html")
        email.send()

        # print("Message Sent Successfully!")
        return redirect("/")

    else:
        return render(request, 'home/index.html', context)

def InstitutePage(request):
    return render(request,'home/InstitutePage.html')

def StudentPage(request):
    return render(request,'home/StudentPage.html')

def TutorPage(request):
    return render(request,'home/TutorPage.html')

# def course_page(request):
#     if not request.GET.get('course_id'):
#         distinct_courses = []
#         categories = Category.objects.filter(available=True)
#         for category in categories:
#             course = Course.objects.filter(
#                 available=True, category=category).first()
#             if course is not None:
#                 distinct_courses.append(course)

#         context = {
#             'courses': Course.objects.filter(available=True),
#             'categories': categories,
#             'dist_courses': distinct_courses
#         }
#         return render(request, "code2learn_app/course.html", context)
#     else:
#         course_id = request.GET['course_id']
#         try:
#             course = Course.objects.get(id=course_id, available=True)
#             context = {
#                 'course': course
#             }
#             return render(request, "code2learn_app/course_detail.html", context)
#         except:
#             raise Http404()


# def Razorpay(request):
#     if request.is_ajax():
#         print("ajax call")
#         fullname = request.POST.get('name')
#         email = request.POST.get('email')
#         phonenum = request.POST.get('phone')
#         collegename = request.POST.get('college')
#         course = request.POST.get('course')
#         amount = request.POST.get('amount')

#         register = Register(full_name=fullname, email=email,
#                             phone_num=phonenum,
#                             college_name=collegename, course=course, amount=amount)
#         register.save()

#         currentid = register.id

#         x = "MS"
#         y = str(currentid + 10000)
#         z = x+y

#         registerobj = Register.objects.get(id=currentid)
#         registerobj.registerid = z
#         registerobj.save()
#         # razorpay integration

#         # step 1: Order id

#         order_amount = registerobj.amount*100
#         order_currency = 'INR'
#         client = razorpay.Client(auth=(KEY_ID, KEY_SECRET))
#         payment = client.order.create(
#             amount=order_amount, currency=order_currency, payment_capture=1)  # return order_id
#         print(payment)
#         return JsonResponse({'payment_id': payment.id})


# def load_courses(request):
#     category_id = request.GET.get('category_id')
#     courses = Course.objects.filter(
#         available=True, category_id=category_id).order_by('-id')
#     courses_list = []
#     for course in courses:
#         data = {}
#         data['value'] = course.id
#         data['text'] = f'{course.course_name} ({course.sub_category})'

#         courses_list.append(data)
#     print(courses_list)
#     temp = set()
#     new_courses_list = []
#     for i in courses_list:
#         if i['text'] not in temp:
#             new_courses_list.append(i)
#             temp.add(i['text'])
#     courses_list = list(new_courses_list)
#     print(courses_list)
#     return JsonResponse({'courses': courses_list})


# def load_languages(request):
#     course_with_subcat = request.GET.get('course_name')
#     if 'Weekday' in str(course_with_subcat):
#         sub_category = 'Weekday'
#         course = str(course_with_subcat).replace(' (Weekday)', '')
#     else:
#         sub_category = 'Weekend'
#         course = str(course_with_subcat).replace(' (Weekend)', '')
#     courses = Course.objects.filter(
#         available=True, course_name=course, sub_category__sub_category_name=sub_category)

#     languages_list = []

#     for course in courses:
#         data = {}
#         data['value'] = course.course_language.id
#         data['text'] = course.course_language.language
#         languages_list.append(data)
#     return JsonResponse({'languages': languages_list})


# def load_amount(request):
#     req_course = request.GET.get('course')
#     language = request.GET.get('language')
#     print(f"Course : {req_course}")
#     print(f"Language : {language}")
#     if 'Weekday' in str(req_course):
#         sub_category = 'Weekday'
#         course = str(req_course).replace(' (Weekday)', '')
#     else:
#         sub_category = 'Weekend'
#         course = str(req_course).replace(' (Weekend)', '')
#     course = Course.objects.get(
#         course_name=course, sub_category__sub_category_name=sub_category, course_language__language=language, available=True)
#     print(f"Price : {course.actual_price}")
#     return JsonResponse({'amount': course.actual_price})


# def check_password(user_pass):
#     pattern = "^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%&_])(?=\S+$).{8,20}$"
#     if re.search(pattern, str(user_pass)):
#         return True
#     else:
#         return False


# @login_excluded(redirect_to='home')
# def register(request):

#     context = {
#         'categories': Category.objects.filter(available=True)
#     }

#     if request.method == "POST":
        
#         if request.is_ajax():
#             print(request.POST)
#             coupen = request.POST.get('coupen')
#             actual_price = request.POST.get('price')
#             print(actual_price)
#             print("coupen", coupen)
#             vouchers = Voucher.objects.all()
#             amount = 0
#             for voucher in vouchers:
#                 print(type(voucher.validity))
#                 if voucher.coupen_code == coupen and voucher.validity >= date.today():
#                     amount = decimal.Decimal(actual_price) - voucher.amount
#             return JsonResponse({'amount': amount})
#         else:
#             fullname = request.POST.get('fullname')
#             email = request.POST.get('email')
#             phonenum = request.POST.get('phone')
#             password = request.POST.get('password')
#             youare = request.POST.get('youare')
#             collegename = request.POST.get('collegename')
#             course_with_subcat = request.POST.get('course')
#             language = request.POST.get('language')

#             if 'Weekday' in str(course_with_subcat):
#                 sub_category = 'Weekday'
#                 course_name = str(course_with_subcat).replace(' (Weekday)', '')
#             else:
#                 sub_category = 'Weekend'
#                 course_name = str(course_with_subcat).replace(' (Weekend)', '')
#             course = Course.objects.get(
#                 available=True, course_name=course_name, sub_category__sub_category_name=sub_category, course_language__language=language)

#             language = request.POST.get('language')
#             amount = request.POST.get('amount')
#             payment_mode = request.POST.get('payment_mode')

#             if not check_user(email):
#                 register = Register(full_name=fullname, email=email,
#                                     phone_num=phonenum,
#                                     college_name=collegename, course=course, amount=amount)
#                 register.save()
#                 print("Helllllllllllllllllllllllllllllllo",youare)
#                 create_new_user(fullname, email, password,
#                                 phonenum, youare, collegename)
#             # else:
#             #     context = {
#             #         'error': 'You are already signed up. Please login to continue.'
#             #     }
#             #     return render(request, 'code2learn_app/register.html', context)

#             else:
#                 try:
#                     if request.session['email']:
#                         register = Register(full_name=request.session['fullname'], email=request.session['email'], phone_num=request.session['phonenum'],
#                                             college_name=collegename, course=course, amount=amount)
#                         register.save()
#                 except KeyError:
#                     error_msg = "You are not logged in. Please login to continue."
#                     return render(request, 'code2learn_app/register.html', {'error': error_msg})

#             currentid = register.id
#             registerobj = Register.objects.get(id=currentid)
#             # select payment mode
#             if payment_mode == 'paytm':

#                 x = "MS"
#                 y = str(currentid + 10000)
#                 z = x+y

#                 registerobj.registerid = z
#                 registerobj.save()

#                 param_dict = {

#                     'MID': MID,
#                     'ORDER_ID': str(registerobj.registerid),
#                     'TXN_AMOUNT': str(registerobj.amount),
#                     'CUST_ID': registerobj.email,
#                     'INDUSTRY_TYPE_ID': 'Retail',
#                     'WEBSITE': 'WEBSTAGING',
#                     'CHANNEL_ID': 'WEB',
#                     'CALLBACK_URL': f'http://{get_current_site(request)}/handlerequest/',

#                 }
#                 param_dict['CHECKSUMHASH'] = generate_checksum(
#                     param_dict, MERCHANT_KEY)
#                 return render(request, 'code2learn_app/paytm.html', {'param_dict': param_dict})

#             elif payment_mode == 'razor':
#                 order_amount = int(registerobj.amount*100)
#                 print(order_amount)
#                 order_currency = 'INR'
#                 client = razorpay.Client(auth=(KEY_ID, KEY_SECRET))

#                 order = client.order.create(
#                     {'amount': order_amount, 'currency': order_currency, 'payment_capture': '1'})
#                 print(order)

#                 registerobj.registerid = order['id']
#                 registerobj.save()

#                 context['payment'] = order
#                 context['name'] = registerobj.full_name
#                 context['phone_num'] = registerobj.phone_num
#                 context['email'] = registerobj.email
#                 context['rzp_id'] = KEY_ID
#                 return render(request, "code2learn_app/razorpay.html", context)

#     else:
#         return render(request, 'code2learn_app/register.html', context)


# def getcontent(request):
#     if request.method == "POST":
#         fullname = request.POST.get('fullname')
#         email = request.POST.get('email')
#         phonenum2 = request.POST.get('phonenum2')
#         print(fullname, email, phonenum2)

#         getcontent = GetContent(full_name=fullname, email=email,
#                                 phone_num=phonenum2)
#         getcontent.save()
#         print("GetContent Saved Successfully!")

#         pdf1 = Pdf.objects.get(id=1)
#         getcontentpath = "/media/"+str(pdf1.get_content)

#         return redirect(getcontentpath)
#     else:
#         return HttpResponse("Invalid")

#         # email1 = (EmailInfo.objects.get(id=1)).attachment.path
#         # response = FileResponse(open(email1, 'rb'))
#         # response = HttpResponse(content_type='pdf/force-download')
#         # return response

#         # email1 = (EmailInfo.objects.get(id=1)).attachment.path
#         # return serve(request, os.path.basename(email1), os.path.dirname(email1))


# @csrf_exempt
# def Razorhandlerequest(request):
#     if request.is_ajax():

#         # from front end
#         payment_id = request.POST.get('payment_id')
#         order_id = request.POST.get('order_id')
#         sign = request.POST.get('sign')
#         server_order = request.POST.get('server_order')

#         # genrate signature
#         secret_key = bytes(KEY_SECRET, 'utf-8')
#         generated_signature = hmac.new(secret_key, bytes(
#             server_order + "|" + payment_id, 'utf-8'), hashlib.sha256).hexdigest()

#         # checking authentic source
#         if generated_signature == sign:
#             print("payment Successfully")
#             orderid = order_id
#             registerobj = Register.objects.get(registerid=orderid)
#             transaction = Transaction(orderid=order_id, mid=payment_id,
#                                       txnamount=registerobj.amount, currency='INR', respmsg=sign, status="success")
#             transaction.save()
#             context = {
#                 'orderid': orderid,
#                 'name': registerobj.full_name,
#                 'college': registerobj.college_name,
#                 'phone': registerobj.phone_num,
#                 'email': registerobj.email,
#                 'course': registerobj.course,
#                 'amount': registerobj.amount,
#                 'date': registerobj.created_at,
#             }

#             print(orderid)
#             create_certificateobj(request, registerobj.full_name, orderid)
#             if check_user(registerobj.email):
#                 user = User.objects.get(email=registerobj.email)
#                 user.registrations.add(
#                     Register.objects.get(registerid=orderid))
#                 user.is_active = True
#                 user.save()

#             return JsonResponse({'success': True})

#         else:
#             print("payment Failure")
#             return JsonResponse({'success': False})

#         # Generate Signature on your Server
#         '''
#         client = razorpay.Client(auth = (KEY_ID, KEY_SECRET))
#         params_dict = {
#             'razorpay_order_id': server_order,
#             'razorpay_payment_id': payment_id,
#             'razorpay_signature': sign
#         }
#         client.utility.verify_payment_signature(params_dict)
#         '''


# @csrf_exempt
# def show_invoice(request, id):
#     registerobj = Register.objects.get(registerid=id)
#     # course = Course.objects.get(
#     #     course_name=registerobj.course, sub_category__sub_category_name=registerobj.sub_category, course_language__language=registerobj.language)
#     context = {
#         'orderid': id,
#         'name': registerobj.full_name,
#         'college': registerobj.college_name,
#         'phone': registerobj.phone_num,
#         'email': registerobj.email,
#         'course': registerobj.course.course_name,
#         'sub_category': registerobj.course.sub_category,
#         'language': registerobj.course.course_language,
#         'amount': registerobj.amount,
#         'date': registerobj.created_at,
#     }
#     return render(request, 'code2learn_app/invoice.html', context)


# @csrf_exempt
# def failed_payment(request):
#     if request.is_ajax():

#         # from front end
#         payment_id = request.POST.get('payment_id')
#         order_id = request.POST.get('order_id')
#         server_order = request.POST.get('server_order')
#         reason = request.POST.get('reason')
#         step = request.POST.get('step')
#         source = request.POST.get('source')
#         description = request.POST.get('description')
#         code = request.POST.get('code')
#         transaction = Transaction.objects.create(paymentmode=code, orderid=order_id, mid=payment_id, txnamount=0, gatewayname=source,
#                                                  currency='INR', respmsg="Step : "+step+" Reason : "+reason+" Desc: "+description, status='Failed')
#         return JsonResponse({'success': True})


# @csrf_exempt
# def handlerequest(request):
#     # paytm will send you post request here
#     form = request.POST
#     response_dict = {}
#     for i in form.keys():
#         print(i)
#         print(form[i])
#         # print(response_dict[i])
#         response_dict[i] = form[i]
#         if i == 'CHECKSUMHASH':
#             checksum = form[i]

#     print(response_dict)

#     # to lowercase the key in dictonary
#     response_dict_lowercase = {k.lower(): v for k, v in response_dict.items()}

#     response_dict_lowercase.pop('checksumhash')

#     print(response_dict_lowercase)

#     transaction = Transaction(**response_dict_lowercase)
#     transaction.save()

#     # print(response_dict['ORDERID'])
#     # print(response_dict['CURRENCY'])
#     # print(response_dict['GATEWAYNAME'])
#     # print(response_dict['RESPMSG'])
#     # print(response_dict['BANKNAME'])
#     # print(response_dict['PAYMENTMODE'])
#     # print(response_dict['MID'])
#     # print(response_dict['RESPCODE'])
#     # print(response_dict['TXNID'])
#     # print(response_dict['TXNAMOUNT'])
#     # print(response_dict['STATUS'])
#     # print(response_dict['BANKTXNID'])
#     # print(response_dict['TXNDATE'])

#     verify = verify_checksum(response_dict, MERCHANT_KEY, checksum)
#     if verify:
#         if response_dict['RESPCODE'] == '01':
#             print('order successful')

#             orderid = response_dict['ORDERID']
#             # currency = response_dict['CURRENCY']
#             # gatewayname = response_dict['GATEWAYNAME']
#             # respmsg = response_dict['RESPMSG']
#             # bankname = response_dict['BANKNAME']
#             # paymentmode = response_dict['PAYMENTMODE']
#             # mid = response_dict['MID']
#             # respcode = response_dict['RESPCODE']
#             # txnid = response_dict['TXNID']
#             txnamount = response_dict['TXNAMOUNT']
#             # status = response_dict['STATUS']
#             # banktxnid = response_dict['BANKTXNID']
#             # txndate = response_dict['TXNDATE']

#             registerobj = Register.objects.get(registerid=orderid)
#             course = Course.objects.get(
#                 course_name=registerobj.course, sub_category__sub_category_name=registerobj.sub_category, course_language__language=registerobj.language)

#             context = {
#                 'orderid': orderid,
#                 'name': registerobj.full_name,
#                 'college': registerobj.college_name,
#                 'phone': registerobj.phone_num,
#                 'email': registerobj.email,
#                 'course': course.course_name,
#                 'sub_category': course.sub_category,
#                 'language': course.course_language,
#                 'amount': registerobj.amount,
#                 'date': registerobj.created_at,
#             }

#             # save details in certificate table

#             create_certificateobj(request, registerobj.full_name, orderid)
#             if check_user(registerobj.email):
#                 user = User.objects.get(email=registerobj.email)
#                 user.registrations.add(
#                     Register.objects.get(registerid=orderid))
#                 user.is_active = True
#                 user.save()

#             # print(context)

#             # transaction = Transaction(orderid=orderid, gatewayname=gatewayname, currency=currency,
#             #                           respmsg=respmsg, bankname=bankname, paymentmode=paymentmode, mid=mid,
#             #                           respcode=respcode, txnid=txnid, txnamount=txnamount, status=status,
#             #                           banktxnid=banktxnid, txndate=txndate)

#             # print(transaction)

#             # transaction.save()

#             # return render(request, 'code2learn_app/paymentstatus.html', {'response': response_dict})

#             return render(request, 'code2learn_app/invoice.html', context)

#         else:
#             print('order was not successful because' +
#                   response_dict['RESPMSG'])

#             # currency = response_dict['CURRENCY']
#             # respmsg = response_dict['RESPMSG']
#             # mid = response_dict['MID']
#             # respcode = response_dict['RESPCODE']
#             # txnid = response_dict['TXNID']
#             # txnamount = response_dict['TXNAMOUNT']
#             # status = response_dict['STATUS']
#             # banktxnid = response_dict['BANKTXNID']

#             # transaction = Transaction(currency=currency,
#             #                           respmsg=respmsg, mid=mid,
#             #                           respcode=respcode, txnid=txnid, txnamount=txnamount, status=status,
#             #                           banktxnid=banktxnid)

#             # transaction.save()

#             return render(request, 'code2learn_app/paymentstatus.html', {'response': response_dict})

#     else:
#         return HttpResponse("Invalid")


# def invoice(request):
#     return render(request, 'code2learn_app/invoice.html')


# # for creating certificate object after successful registration

# def create_certificateobj(request, name, register_num):
#     certificate_num = ''.join(random.choices(
#         string.ascii_uppercase + string.digits, k=8))
#     print(certificate_num)
#     link = f"https://{get_current_site(request)}/certificate/{certificate_num}"
#     try:
#         certificateobj = Certificate(
#             certificate_num=certificate_num, register_num=register_num)
#         qr_obj = Qrcode(name=name, link=link, certificate_num=certificate_num)
#         certificateobj.save()
#         qr_obj.save()
#     except IntegrityError:
#         create_certificateobj()


# # exception 404 view
# def error_404(request, exception):

#     data = {}
#     return render(request, 'code2learn_app/404.html', data)

# # exception 500 view


# def error_500(request):
#     data = {}
#     return render(request, 'code2learn_app/500.html', data)


# def career(request):
#     return render(request, 'code2learn_app/career.html')


# def course_search(request):
#     search_query = request.GET.get('query')
#     courses = Course.objects.filter(Q(course_name__icontains=search_query) | Q(category__category_name__icontains=search_query) | Q(
#         sub_category__sub_category_name__icontains=search_query), available=True).distinct()
#     context = {
#         'search_query': search_query,
#         'search_results': courses
#     }
#     return render(request, "code2learn_app/course_search.html", context)


# def enroll_course(request, course_id):
#     context = {}
#     try:
#         course = Course.objects.get(id=course_id)
#         context['course'] = course
#         email = request.session.get('email')
#         # Check if user has already registered for a course
#         if Register.objects.filter(email=email, course__id=course_id).exists():
#             error = 'You are already subscribed to this course.'
#             context['error'] = error
#     except:
#         raise Http404()
    
#     if request.method == "POST":
#         global amount
#         if request.is_ajax():
#             coupon = request.POST.get('coupon')
#             actual_price = course.actual_price
#             print(actual_price)
#             vouchers = Voucher.objects.all()
#             amount = 0
#             for voucher in vouchers:
#                 if voucher.coupen_code == coupon and voucher.validity >= date.today():
#                     amount = decimal.Decimal(
#                         actual_price) - decimal.Decimal(voucher.amount)
#             return JsonResponse({'amount': amount})
#         else:
#             user = User.objects.get(email=request.session['email'])
#             fullname = user.full_name
#             email = user.email
#             phonenum = user.phone_num
#             amount = request.POST.get('price')
#             coupon = request.POST.get('coupon')
#             print(coupon)
#             print(amount)
#             course = Course.objects.get(id=course_id)
#             payment_mode = request.POST.get('payment_mode')
#             register = Register(full_name=fullname, email=email, phone_num=phonenum,
#                                 college_name=user.institution, course=course, amount=amount)
#             register.save()
#             currentid = register.id
#             registerobj = Register.objects.get(id=currentid)
#             # select payment mode
#             if payment_mode == 'paytm':

#                 x = "MS"
#                 y = str(currentid + 10000)
#                 z = x+y

#                 registerobj.registerid = z
#                 registerobj.save()

#                 param_dict = {

#                     'MID': MID,
#                     'ORDER_ID': str(registerobj.registerid),
#                     'TXN_AMOUNT': str(registerobj.amount),
#                     'CUST_ID': registerobj.email,
#                     'INDUSTRY_TYPE_ID': 'Retail',
#                     'WEBSITE': 'WEBSTAGING',
#                     'CHANNEL_ID': 'WEB',
#                     'CALLBACK_URL': f'http://{get_current_site(request)}/handlerequest/',

#                 }
#                 param_dict['CHECKSUMHASH'] = generate_checksum(
#                     param_dict, MERCHANT_KEY)
#                 return render(request, 'code2learn_app/paytm.html', {'param_dict': param_dict})

#             elif payment_mode == 'razor':
#                 order_amount = int(registerobj.amount*100)
#                 print(order_amount)
#                 order_currency = 'INR'
#                 client = razorpay.Client(auth=(KEY_ID, KEY_SECRET))

#                 order = client.order.create(
#                     {'amount': order_amount, 'currency': order_currency, 'payment_capture': '1'})
#                 print(order)

#                 registerobj.registerid = order['id']
#                 registerobj.save()

#                 context['payment'] = order
#                 context['name'] = registerobj.full_name
#                 context['phone_num'] = registerobj.phone_num
#                 context['email'] = registerobj.email
#                 context['rzp_id'] = KEY_ID
#                 return render(request, "code2learn_app/razorpay.html", context)
#     return render(request, "code2learn_app/enroll.html", context)
