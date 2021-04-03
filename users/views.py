from code2learn_app.models import Register
from django.shortcuts import render, redirect, HttpResponseRedirect
from .models import OTPModel, User
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password, check_password
import json
from django.views import View
from random import randint
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.utils.decorators import method_decorator
from code2learn_app.middlewares.auth import login_excluded
import re


# Create your views here.
def check_user(email):
    return User.objects.filter(email=email).exists()


def create_new_user(full_name, email, password, phone_num, user_type, institution):
    print("Hellllllllllo",user_type)
    user = User(full_name=full_name, email=email,
                password=password, phone_num=phone_num, user_type=user_type, institution=institution)
    user.password = make_password(user.password)
    user.is_active = False
    user.save()


def email_validation(request):
    data = json.loads(request.body)
    email = data['email']
    if User.objects.filter(email=email).exists():
        return JsonResponse({'email_error': 'You are already registered. Please login to continue.'}, status=409)
    return JsonResponse({'email_valid': True})

def password_validation(request):
    data = json.loads(request.body)
    password = data['password']
    pattern = '^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%&_])(?=\S+$).{8,20}$'
    if bool(re.match(pattern,password)):
        return JsonResponse({'password_valid': True})
    else:
        return JsonResponse({'password_error': 'Password must be 8-20 characters long and must contain atleast one uppercase letter, one lowercase letter, one number(0-9) and one special character(@,#,$,%,&,_)'})

def find_email(request):
    data = json.loads(request.body)
    email = data['email']
    if not User.objects.filter(email=email).exists():
        return JsonResponse({'email_error': 'You are not registered. Please signup to continue.'}, status=404)
    return JsonResponse({'email_valid': True})


class Login(View):
    return_url = None

    @method_decorator(login_excluded(redirect_to='home'))
    def get(self, request):
        Login.return_url = request.GET.get('return_url')
        return render(request, "login.html")

    @method_decorator(login_excluded(redirect_to='home'))
    def post(self, request):
        email = request.POST['email']
        password = request.POST['password']
        error_msg = None
        if check_user(email):
            user = User.objects.get(email=email)
            flag = check_password(password, user.password)
            if flag:
                request.session['user'] = user.id
                request.session['fullname'] = user.full_name
                request.session['email'] = user.email
                request.session['phonenum'] = user.phone_num
                if Login.return_url:
                    return HttpResponseRedirect(Login.return_url)
                else:
                    Login.return_url = None
                    return redirect('home')
                    # return render(request, "code2learn_app/index.html", {'user': user})
            else:
                error_msg = "Password is incorrect."
        else:
            error_msg = "You are not registered yet."
        return render(request, "login.html", {'error': error_msg})


def logout(request):
    request.session.clear()
    return redirect('login')


def gen_otp():
    return randint(100000, 999999)


def send_otp(request):
    user_email = request.GET['email']
    # Get user
    user = User.objects.get(email=user_email)
    otp = gen_otp()     # Generate OTP
    # Save OTP in database and send email to user
    try:
        OTPModel.objects.create(user=user, otp=otp)
        data = {
            'receiver': user.full_name.split(" ")[0].capitalize(),
            'otp': otp
        }
        html_content = render_to_string("emails/otp.html", data)
        text_content = strip_tags(html_content)

        email = EmailMultiAlternatives(
            f"One Time Password | Code2Learn",
            text_content,
            "Code2Learn <contact@code2learn.co>",
            [user_email]
        )
        print("sending email")
        email.attach_alternative(html_content, "text/html")
        email.send()
        print("Sent")
        return JsonResponse({'otp_sent': f'An OTP has been sent to {user_email}.'})
    except Exception:
        return JsonResponse({'otp_error': 'Error while sending OTP, try again'})


def match_otp(email, otp):
    otp_from_db = OTPModel.objects.filter(user__email=email).last().otp
    return str(otp) == str(otp_from_db)


def check_otp(request):
    req_otp = request.GET['otp']
    req_user = request.GET['email']
    if match_otp(req_user, req_otp):
        return JsonResponse({'otp_match': True})
    else:
        return JsonResponse({'otp_mismatch': 'OTP does not match.'})


def forgot_password(request):
    if request.method == "POST":
        try:
            password = request.POST.get('password')
            email = request.POST.get('email')
            user = User.objects.get(email=email)
            user.set_password(password)
            user.save()
            return render(request, "login.html", {"message": "Password changed successfully. You can now login with your new password."})
        except:
            return render(request, "reset-password.html", {"error": "Password could not be changed, please try again."})
    return render(request, "reset-password.html")