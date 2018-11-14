from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail
from django.conf import settings
from . import forms
from .models import DefaultUser, News
from Gku.crypto import AESCipher
import datetime, urllib.parse

"""  
from LandPage.mail import sendMail

send_mail(
    'Subject here',
    'Here is the message.',
    'from@example.com',
    ['to@example.com'],
    fail_silently=False,
)
"""

def index(request):
    if 'id' not in request.session:
        news = News.objects.all()
        return render(request, 'LandPage/wrapper.html', {'news': news})
    id = request.session['id']
    user = DefaultUser.objects.get(id=id)
    if user.activationType != 0:
        return HttpResponseRedirect('/confirmation')
    return HttpResponseRedirect('/account')

def login(request):
    if 'id' in request.session:
        return HttpResponseRedirect('/index')
    if request.method == 'POST':
        form = forms.Login(request.POST)
        #if forms.is_valid():
        login = request.POST['login']
        password = request.POST['password']
        return HttpResponse(login + password)
    return render(request, 'Login/wrapper.html')

def register(request):
    if 'id' in request.session:
        return HttpResponseRedirect('/index')
    err = ""
    if request.method == 'POST':
        form = forms.CreateUser(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            if not user.chkLoginReg():
                err = "Логин не подходит по регулярке"
            elif not user.chkPass():
                err = "Пароль не подходит по регулярке"
            elif not user.chkMail():
                err = "Мыло не подходит по регулярке"
            else:
                mail = user.mail
                user.encrypt()
                if not DefaultUser.chkExistLogin(user.login):
                    err = "Такой логин уже существует"
                elif not DefaultUser.chkExistMail(user.mail):
                    err = "Аккаунт с такой почтой уже зарегистрирован!"
                else:
                    user.genActivationKey(1)
                    key = urllib.parse.quote(user.encActivationKey())
                    user.setCreationDate()
                    user.save()

                    encID = urllib.parse.quote(user.getEncID())

                    send_mail(
                        'Активация аккаунта',
                        'http://' + settings.HOSTNAME + '/activateAccount?id=' + encID + '&key=' + key,
                        'cypherdesk.isyn@gmail.com',
                        [mail,],
                    )

                    return HttpResponseRedirect('/confirmation')
    else:
        form = forms.CreateUser()
    return render(request, 'Register/wrapper.html', {'form': form, 'ok': err == "", 'err': err})


def activateAccount(request):
    if 'id' not in request.GET or 'key' not in request.GET:
        return HttpResponse('Error')
    encID, key = request.GET['id'], request.GET['key']

    aes = AESCipher(settings.AES_ID_KEY)

    try:
        id = aes.decrypt(urllib.parse.unquote(encID))
    except UnicodeDecodeError:
        return render(request, 'Confirm/error.html', {'error_msg': 'Неверный ключ'})
    except:
        return render(request, 'Confirm/error.html', {'error_msg': 'Ууупс... Ошибка!'})

    user = DefaultUser.objects.get(id=id)

    if user.activationType != 1:
        return HttpResponseRedirect('/')

    aes = AESCipher(settings.AES_ACTIVATION_KEY)

    try:
        key = aes.decrypt(urllib.parse.unquote(key))
    except UnicodeDecodeError:
        return render(request, 'Confirm/error.html', {'error_msg': 'Неверный ключ'})
    except:
        return render(request, 'Confirm/error.html', {'error_msg': 'Ууупс... Ошибка!'})

    if user.activationKey == key:
        DefaultUser.objects.filter(id=id).update(activationType=0)
        request.session['id'] = user.id
        return HttpResponseRedirect('/')
    return render(request, 'Confirm/error.html', {'error_msg': 'Неверный ключ'})

def news(request):
    if 'id' not in request.GET:
        return HttpResponse('Error')
    newsID = request.GET['id']
    news = News.objects.get(id=newsID)
    return HttpResponse(news.title + ' ' + news.detailedNews)

def confirmation(request):
    return render(request, 'Confirm/info.html')

def logout(request):
    if 'id' in request.session:
        del request.session['id']
    return HttpResponseRedirect('/')

def error_500(request):
    return render(request, '500/error_500.html')

def error_404(request, exception):
    return render(request, '404/error_404.html')

def test(request):
    return HttpResponse("OK")