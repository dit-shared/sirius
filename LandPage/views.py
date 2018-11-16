from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail
from django.conf import settings
from . import forms
from .models import DefaultUser, News, StandartDecryptField, StandartEncryptField, HashPassword
from Gku.crypto import AESCipher
import datetime, urllib.parse, os

def index(request):
    if 'id' not in request.session:
        news = News.objects.all().order_by('-id')[:6]
        return render(request, 'LandPage/wrapper.html', {'news': news})
    return HttpResponseRedirect('/account')

def login(request):
    errors = list()
    if 'id' in request.session:
        return HttpResponseRedirect('/account')
    if request.method == 'POST':
        form = forms.Login(request.POST)
        if form.is_valid():
            login = StandartEncryptField(request.POST['login'], settings.AES_DEFAULT_KEY)
            password = HashPassword(request.POST['password'])

            if DefaultUser.objects.filter(login=login).exists():
                user = DefaultUser.objects.get(login=login)
                if password != StandartDecryptField(user.password, settings.AES_DEFAULT_KEY):
                    errors.append('Неправильный логин или пароль')
                else:
                    if user.activationType == 1:
                        return HttpResponseRedirect('/confirmation')
                    request.session['id'] = user.id
                    return HttpResponseRedirect('/account')
            else:
                errors.append('Такого пользователя не существует')
    else:
        form = forms.Login()
    forgotForm = forms.ForgotPass()
    return render(request, 'Login/wrapper.html', {'form': form, 'forgotForm': forgotForm, 'ok': len(errors) == 0, 'errors': errors})

def register(request):
    if 'id' in request.session:
        return HttpResponseRedirect('/index')
    errors = list()
    if request.method == 'POST':
        form = forms.CreateUser(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            if not user.chkLoginReg():
                errors.append("Логин не подходит по регулярке")
            elif not user.chkPass():
                errors.append("Пароль не подходит по регулярке")
            elif not user.chkMail():
                errors.append("Мыло не подходит по регулярке")
            elif user.password != request.POST['repass']:
                errors.append("Пароли не совпадают!")
            else:
                mail = user.mail
                user.hashPass()
                user.encrypt()
                if not DefaultUser.chkExistLogin(user.login):
                    errors.append("Такой логин уже существует")
                elif not DefaultUser.chkExistMail(user.mail):
                    errors.append("Аккаунт с такой почтой уже зарегистрирован!")
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
    return render(request, 'Register/wrapper.html', {'form': form, 'ok': len(errors) == 0, 'errors': errors})


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
        return HttpResponseRedirect('/login')
    return render(request, 'Confirm/error.html', {'error_msg': 'Неверный ключ'})

def forgotPassword(request):
    if 'id' in request.session:
        return HttpResponseRedirect('/account')
    if 'mail' not in request.POST:
        return HttpResponse('Error')
    requisites = request.POST['mail']

def news(request):
    if 'id' not in request.GET:
        return HttpResponse('Error')
    newsID = request.GET['id']
    if News.objects.filter(id=newsID).exists():
        news = News.objects.get(id=newsID)
        return render(request, 'News/index.html', {'news': news})
    return render(request, '404/error_404.html')

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
    str = os.path.join(settings.BASE_DIR, 'static/')
    return HttpResponse("OK")