from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from LandPage.models import DefaultUser, StandartEncryptField, HashPassword
from .models import ExtUser
from Account import forms
from Gku import settings
import base64

def changeExtUserInfo(request):
    if 'id' not in request.session:
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        errors = list()
        extUserForm = forms.ChangeExtUserInfo(request.POST, request.FILES)
        if extUserForm.is_valid():
            extUser = extUserForm.save(commit=False)
            extUser.user_id = request.session['id']

            if extUser.phone != "" and not extUser.chkPhoneNumber():
                errors.append('Неправильный номер телефона!')
            if extUser.total_square != None:
                if extUser.total_square < 1:
                    errors.append('Некорректное значение площади')
            if extUser.cnt_fiodr != None:
                if extUser.cnt_fiodr < 1:
                    errors.append('Некорректное количество проживающих')

            print(extUser.cnt_fiodr, extUser.total_square)

            if len(errors) == 0:
                if ExtUser.objects.filter(user_id=extUser.user_id).exists():
                    tmpExtUser = ExtUser.objects.get(user_id=extUser.user_id)
                    if extUser.phone == "":
                        extUser.phone = tmpExtUser.phone
                    if extUser.adress == "":
                        extUser.adress = tmpExtUser.phone
                    if not extUser.ava:
                        extUser.ava = tmpExtUser.ava
                    if extUser.cnt_fiodr != None:
                            extUser.cnt_fiodr = tmpExtUser.cnt_fiodr
                    if extUser.total_square != None:
                        extUser.total_square = tmpExtUser.total_square
                    tmpExtUser.delete()

                extUser.save()

                return render(request, 'OK/index.html', {'title': 'Отлично!', 'msg': 'Ваши данные успешно изменены.', 'link': 'account'})

        defaultUserInfoForm = forms.ChangeUserInfo()
        changePassForm = forms.ChangePassword()
        changeMailForm = forms.ChangeMail()
        return render(request, 'AccountSettings/index.html',
                     {'defUserInfo': defaultUserInfoForm, 'extUserInfo': extUserForm,
                     'changePass': changePassForm, 'changeMail': changeMailForm, 'extUserInfoErrors': errors,})
    return HttpResponseRedirect('/account')

def changeStandartUserInfo(request):
    if 'id' not in request.session:
        return HttpResponseRedirect('/account')
    if request.method == "POST":
        errors = list()
        defaultUserInfoForm = forms.ChangeUserInfo(request.POST)
        if defaultUserInfoForm.is_valid():
            userInfo = defaultUserInfoForm.save(commit=False)
            userInfo.user_id = request.session['id']

            user = DefaultUser.objects.get(id=userInfo.user_id)
            if userInfo.name != "":
                user.name = StandartEncryptField(userInfo.name, settings.AES_DEFAULT_KEY)
            if userInfo.surname != "":
                user.surname = StandartEncryptField(userInfo.surname, settings.AES_DEFAULT_KEY)
            if userInfo.patronymic != "":
                user.patronymic = StandartEncryptField(userInfo.patronymic, settings.AES_DEFAULT_KEY)

            user.save()
            return render(request, 'OK/index.html', {'title': 'Отлично!', 'msg': 'Ваши данные успешно изменены.', 'link': 'account'})
        else:
            changePassForm = forms.ChangePassword()
            changeMailForm = forms.ChangeMail()
            extUserForm = forms.ExtUser()
            return render(request, 'AccountSettings/index.html',
                          {'defUserInfo': defaultUserInfoForm, 'extUserInfo': extUserForm,
                           'changePass': changePassForm, 'changeMail': changeMailForm, 'extUserInfoErrors': errors, })
    return HttpResponseRedirect('/account')

def changePassword(request):
    if 'id' not in request.session:
        return HttpResponseRedirect('/logout')
    if request.method == 'POST':
        errors = list()
        changePassForm = forms.ChangePassword(request.method)
        if changePassForm.is_valid():
            oldpass = request.POST['oldpass']
            newpass = request.POST['newpass']
            repass = request.POST['repass']

            user = DefaultUser.objects.filter(id=request.session['id'])
            user.decrypt()

            hashedOldPass = HashPassword(oldpass)
            if hashedOldPass != oldpass:
                errors.append('Неверный пароль!')
            else:
                if newpass != repass:
                    errors.append('Новые пароли не совпадают!')
                else:
                    DefaultUser.objects.get(id=request.session['id']).update(password=StandartEncryptField(HashPassword(newpass), settings.AES_DEFAULT_KEY))
                    return render(request, 'OK/index.html', {'title': 'Отлично!', 'msg': 'Ваш пароль успешно изменен.', 'link': 'account'})
        changePassForm = forms.ChangePassword()
        changeMailForm = forms.ChangeMail()
        extUserForm = forms.ExtUser()
        defaultUserInfoForm = forms.DefaultUser()
        return render(request, 'AccountSettings/index.html',
                      {'defUserInfo': defaultUserInfoForm, 'extUserInfo': extUserForm,
                       'changePass': changePassForm, 'changeMail': changeMailForm, 'extUserInfoErrors': errors, })
def test(request):
    v = 'asd'
    b = base64.b64encode(v)
    print(v)
    return HttpResponse(StandartEncryptField('dfs', settings.AES_DEFAULT_KEY))