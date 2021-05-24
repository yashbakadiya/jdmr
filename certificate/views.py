from django.http.response import HttpResponse
from django.shortcuts import render, redirect

from .models import Certificate, Qrcode, Certificate_sign
from code2learn_app.models import Register


# Create your views here.

def index(request):
    context = {
        'title': 'No Certificate Found',
        'error': "We could not find any certificate."
    }
    return render(request, 'certificate/404.html', context)


def certificatenum(request, certificate_num):
    try:
        certificateobj = Certificate.objects.get(
            certificate_num=certificate_num)
        if(certificateobj.issued):
            registerobj = Register.objects.get(
                registerid=certificateobj.register_num)
            qrcodeobj = Qrcode.objects.get(certificate_num=certificate_num)
            sign = Certificate_sign.objects.last()
            context = {
                'fullname': registerobj.full_name,
                'course': registerobj.course,
                'qrcodeobj': qrcodeobj,
                'sign': sign,
                'issue_date': certificateobj.issued_date
            }
            return render(request, 'certificate/certificate.html', context)
        else:
            context = {
                'title': 'No Certificate Found',
                'error': "We could not find any certificate."
            }
            return render(request, 'certificate/404.html', context)

    except Certificate.DoesNotExist as e:
        context = {
            'title': 'No Certificate Found',
            'error': "We could not find any certificate."
        }
    return render(request, 'certificate/404.html', context)


def view_certi(request):
    if 'number' in request.GET:
        certificate_no = request.GET['number']
        certificate_no = certificate_no.strip()
        return redirect('certificatenum', certificate_num=certificate_no)
    return render(request, 'certificate/certificateview.html')
