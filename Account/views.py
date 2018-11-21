from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from LandPage.models import DefaultUser
from .models import ExtUser
import Account.forms as forms

def index(request):
    if 'id' not in request.session:
        return HttpResponseRedirect('/')
    id = request.session['id']

    if not DefaultUser.objects.filter(id=id).exists():
        return HttpResponseRedirect('/logout')

    user = DefaultUser.objects.get(id=id)
    user.decrypt()

    extUser = ExtUser()
    if ExtUser.objects.filter(user_id=id).exists():
        extUser = ExtUser.objects.get(user_id=id)

    return render(request, 'FrontPage/index.html', {'user': user, 'extUser': extUser})

def electricity(request):
    return render(request, 'Electricity/index.html')

def water(request):
    return render(request, 'Water/index.html')

def changeMode(request):
    return render(request, 'Mode/index.html')

def predictElectricity(request):
    return render(request, 'PredictElectricity/index.html')

def predictWater(request):
    return render(request, 'PredictWater/index.html')

def settings(request):
    defaultUserInfoForm = forms.ChangeUserInfo()
    extUserInfoForm = forms.ChangeExtUserInfo()
    changePassForm = forms.ChangePassword()
    changeMailForm = forms.ChangeMail()
    return render(request, 'AccountSettings/index.html', {'defUserInfo': defaultUserInfoForm, 'extUserInfo': extUserInfoForm,
                                                          'changePass': changePassForm, 'changeMail': changeMailForm})