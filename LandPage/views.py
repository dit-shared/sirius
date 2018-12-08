from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail
from django.conf import settings
from . import forms
from .models import DefaultUser, News, StandartDecryptField, StandartEncryptField, HashPassword, Subscriber
from Gku.crypto import AESCipher
import datetime, urllib.parse, os, re
from Gku import yandexAPI

def index(request):
    if 'id' not in request.session:
        news = News.objects.all().order_by('-id')[:6]
        return render(request, 'LandPage/wrapper.html', {'news1': news[:3], 'news2': news[3:6], 'showMsg': False})
    return HttpResponseRedirect('/account')

def gallery(request):
    return render(request, 'Gallery/index.html')

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
                try:
                    decPass = StandartDecryptField(user.password, settings.AES_DEFAULT_KEY)
                    if password != decPass:
                        errors.append('Неправильный логин или пароль')
                    else:
                        if user.activationType == 1:
                            return HttpResponseRedirect('/confirmation')
                        request.session['id'] = user.id
                        return HttpResponseRedirect('/account')
                except:
                    errors.append('Неправильный логин или пароль')
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
                        'mail@mos-ai.ru',
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


    if DefaultUser.objects.filter(id=id).exists():
        user = DefaultUser.objects.get(id=id)
    else:
        return render(request, 'Confirm/error.html', {'error_msg': 'Ууупс... Ошибка!'})

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
    forgotForm = forms.ForgotPass(request.POST)
    errors = list()
    if forgotForm.is_valid():
        requisites = StandartEncryptField(request.POST['mail'], settings.AES_DEFAULT_KEY)

        if DefaultUser.objects.filter(mail=requisites).exists():
            user = DefaultUser.objects.get(mail=requisites)
        elif DefaultUser.objects.filter(login=requisites).exists():
            user = DefaultUser.objects.get(login=requisites)
        else:
            errors.append('Такого пользователя не существует!')

        if len(errors) == 0:
            key = user.genActivationKey(2)
            encID = urllib.parse.quote(user.getEncID())
            user.save()

            encKey = urllib.parse.quote(StandartEncryptField(key, settings.AES_ACTIVATION_KEY))
            user.decrypt()

            send_mail(
                'Восстановление пароля',
                'http://' + settings.HOSTNAME + '/accountRecover?id=' + encID + '&key=' + encKey,
                'cypherdesk.isyn@gmail.com',
                [user.mail, ],
            )
            return HttpResponseRedirect('/confirmation')
    else:
        forgotForm = forms.ForgotPass()
        errors.append('Заполните капчу')

    form = forms.Login()
    return render(request, 'Login/wrapper.html', {'form': form, 'forgotForm': forgotForm, 'ok2': len(errors) == 0, 'forgotFormErrors': errors})

def accountRecover(request):
    if 'id' not in request.GET or 'key' not in request.GET:
        return HttpResponseRedirect('/')
    encID, encKey = request.GET['id'], request.GET['key']

    aes = AESCipher(settings.AES_ID_KEY)

    try:
        id = aes.decrypt(urllib.parse.unquote(encID))
    except UnicodeDecodeError:
        return render(request, 'Confirm/error.html', {'error_msg': 'Неверный ключ'})
    except:
        return render(request, 'Confirm/error.html', {'error_msg': 'Ууупс... Ошибка!'})

    if DefaultUser.objects.filter(id=id).exists():
        user = DefaultUser.objects.get(id=id)
    else:
        return render(request, 'Confirm/error.html', {'error_msg': 'Ууупс... Ошибка!'})

    if user.activationType != 2:
        return HttpResponseRedirect('/')

    aes = AESCipher(settings.AES_ACTIVATION_KEY)

    try:
        key = aes.decrypt(urllib.parse.unquote(encKey))
    except UnicodeDecodeError:
        return render(request, 'Confirm/error.html', {'error_msg': 'Неверный ключ'})
    except:
        return render(request, 'Confirm/error.html', {'error_msg': 'Ууупс... Ошибка!'})

    if user.activationKey == key:
        form = forms.RecoverForm()
        request.session['enc_id'] = encID
        request.session['key'] = encKey
        return render(request, 'Register/recover.html', {'form': form})
    return render(request, 'Confirm/error.html', {'error_msg': 'Ууупс... Ошибка!'})

def changePass(request):
    if 'enc_id' not in request.session or 'key' not in request.session:
        return HttpResponseRedirect('/')
    encID, encKey = request.session['enc_id'], request.session['key']

    del request.session['enc_id']
    del request.session['key']

    aes = AESCipher(settings.AES_ID_KEY)
    try:
        id = aes.decrypt(urllib.parse.unquote(encID))
    except UnicodeDecodeError:
        return render(request, 'Confirm/error.html', {'error_msg': 'Неверный ключ'})
    except:
        return render(request, 'Confirm/error.html', {'error_msg': 'Ууупс... Ошибка!'})

    if DefaultUser.objects.filter(id=id).exists():
        user = DefaultUser.objects.get(id=id)
    else:
        return render(request, 'Confirm/error.html', {'error_msg': 'Ууупс... Ошибка!'})

    if user.activationType != 2:
        return HttpResponseRedirect('/')

    aes = AESCipher(settings.AES_ACTIVATION_KEY)

    try:
        key = aes.decrypt(urllib.parse.unquote(encKey))
    except UnicodeDecodeError:
        return render(request, 'Confirm/error.html', {'error_msg': 'Неверный ключ'})
    except:
        return render(request, 'Confirm/error.html', {'error_msg': 'Ууупс... Ошибка!'})

    if user.activationKey == key:
        errors = list()
        form = forms.RecoverForm(request.POST)
        if form.is_valid():
            if request.POST['password'] != request.POST['repass']:
                errors.append('Пароли не совпадают!')
            else:
                user.activationKey = ""
                user.activationType = 0
                user.password = request.POST['password']
                user.hashPass()
                user.password = StandartEncryptField(user.password, settings.AES_DEFAULT_KEY)
                user.save()
                return HttpResponseRedirect('/login')
        else:
            form = forms.RecoverForm()
        return render(request, 'Register/recover.html', {'form': form, 'errors': errors})
    return render(request, 'Confirm/error.html', {'error_msg': 'Ууупс... Ошибка!'})


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

def subscribe(request):
    if 'id' not in request.session:
        news = News.objects.all().order_by('-id')[:3]
        msgType, msg, msgTitle = 'success', 'Спасибо за подписку!', 'Отлично!'

        if 'mail' not in request.POST:
            return HttpResponseRedirect('/index')

        mail = request.POST['mail']
        if not chkMail(mail):
            msgTitle = 'Ой, ошибочка...'
            msg = 'Введите правильный почтовый адрес!'
            msgType = 'error'

        if Subscriber.objects.filter(mail=mail).exists():
            msgType = 'info'
            msg = 'Вы уже подписаны на рассылку!'
            msgTitle = 'Спасибо!'
        else:
            s = Subscriber()
            s.mail = mail
            s.save()

        return render(request, 'LandPage/wrapper.html', {'news': news, 'showMsg': True, 'msg': msg, 'msgType': msgType, 'msgTitle': msgTitle})
    return HttpResponseRedirect('/account')

def chkMail(mail):
    if re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", mail):
        return True
    return False

def test(request):
#    user = DefaultUser()
 #   user.login = 'ishbulatov'
#    user.password = 'j4jk56gq'
#    user.mail = 'ishbulatov@mos-ai.ru'
#    user.hashPass()
#    user.encrypt()
#    user.save()
#    user.login = 'lysenko'
#    user.password = 'lysenko'
#    user.mail = 'lysenko@mos-ai.ru'
#    user.hashPass()
#    user.encrypt()
#    user.save()
#    user.login = 'blinova'
#    user.password = '2xuaw7gc'
#    user.mail = 'blinova@mos-ai.ru'
#    user.hashPass()
#    user.encrypt()
#    user.save()
#    user.login = 'korolev'
#    user.password = '1zgxtfrv'
#    user.mail = 'korolev@mos.ru'
#    user.hashPass()
#    user.encrypt()
#    user.save()
#    user.login = 'user_user'
#    user.password = 'alk12qrk'
#    user.mail = 'user_user@mos.ru'
 #   user.hashPass()
  #  user.encrypt()
  #  user.save()
    user = DefaultUser()
    user.login = 'sirius'
    user.password = 'sirius'
    user.mail = 'sirius@mos-ai.ru'
    user.hashPass()
    user.encrypt()
    user.save()
    return HttpResponse(user)
