from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings

""" tmp """
from LandPage.mail import sendMail

def index(request):
    return render(request, 'LandPage/wrapper.html')

def aboutus(request):
    return render(request, 'AboutUs/wrapper.html')

def login(request):
    if request.POST:
        login = request.POST['login']
        password = request.POST['password']
        return HttpResponse(login + "\n" + password)
    return render(request, 'Login/wrapper.html')

def register(request):
    if request.POST:
        login = request.POST['login']
        password = request.POST['password']
        mail = request.POST['mail']
        return HttpResponse(login + password + mail)
    return render(request, 'Register/wrapper.html')

def error_500(request):
    return render(request, '500/error_500.html')

def error_404(request, exception):
    return render(request, '404/error_404.html')

def test(request):
    send_mail(
        subject='Subject here',
        message='kekLOL',
        html_message='<h1>sdfsdf</h1>',
        from_email='jkumoscow@gmail.com',
        recipient_list=['nikita.surnachev03@gmail.com'],
        fail_silently=False,
    )
    return HttpResponse('OK')