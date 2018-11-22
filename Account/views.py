from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from LandPage.models import DefaultUser
from .models import ExtUser, FeedbackRecord, WaterMeters, ElectricityMeters
import Account.forms as forms
from Gku.TelegramBotClass import send as SendTelegram
from Gku import settings as GkuSettings
from Gku import yandexAPI

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

    coords = {'l': 0, 'p': 0}
    # if extUser.adress != '':
    #     resp = yandexAPI.getCoord(extUser.adress).split(' ')
    #     coords['l'] = resp[0]
    #     coords['p'] = resp[1]

    feedbackForm = forms.SendFeedback()
    return render(request, 'FrontPage/index.html', {'user': user, 'extUser': extUser, 'feedbackForm': feedbackForm, 'coords': coords})

def calendar(request):
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

    feedbackForm = forms.SendFeedback()
    return render(request, 'Calendar/index.html', {'user': user, 'extUser': extUser, 'feedbackForm': feedbackForm})

def electricity(request):
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

    feedbackForm = forms.SendFeedback()
    meters = ElectricityMeters.objects.filter(user_id=id)

    for meter in meters:
        meter.date = '{:%Y-%m}'.format(meter.date)

    return render(request, 'Electricity/index.html', {'user': user, 'extUser': extUser, 'feedbackForm': feedbackForm, 'meters': meters})

def water(request):
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

    feedbackForm = forms.SendFeedback()
    meters = WaterMeters.objects.filter(user_id=id)

    for meter in meters:
        meter.date = '{:%Y-%m}'.format(meter.date)

    return render(request, 'Water/index.html', {'user': user, 'extUser': extUser, 'feedbackForm': feedbackForm, 'meters': meters})

def changeMode(request):
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

    feedbackForm = forms.SendFeedback()
    return render(request, 'Mode/index.html', {'user': user, 'extUser': extUser, 'feedbackForm': feedbackForm})

def predictElectricity(request):
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

    feedbackForm = forms.SendFeedback()
    return render(request, 'PredictElectricity/index.html', {'user': user, 'extUser': extUser, 'feedbackForm': feedbackForm})

def predictWater(request):
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

    feedbackForm = forms.SendFeedback()
    return render(request, 'PredictWater/index.html', {'user': user, 'extUser': extUser, 'feedbackForm': feedbackForm})


def uploadData(request):
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

    feedbackForm = forms.SendFeedback()
    addWaterForm = forms.AddWaterMeter()
    addElectForm = forms.AddElecticityMeter()
    return render(request, 'UploadData/index.html', {'user': user, 'extUser': extUser, 'feedbackForm': feedbackForm,
                                                     'addWaterForm': addWaterForm, 'addElectForm': addElectForm})

def settings(request):
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

    defaultUserInfoForm = forms.ChangeUserInfo()
    extUserInfoForm = forms.ChangeExtUserInfo()
    changePassForm = forms.ChangePassword()
    changeMailForm = forms.ChangeMail()
    feedbackForm = forms.SendFeedback()
    return render(request, 'AccountSettings/index.html', {'defUserInfo': defaultUserInfoForm, 'extUserInfo': extUserInfoForm,
                                                          'changePass': changePassForm, 'changeMail': changeMailForm,
                                                           'user': user, 'extUser': extUser, 'feedbackForm': feedbackForm})

def feedback(request):
    if 'id' not in request.session:
        return HttpResponseRedirect('/')
    id = request.session['id']

    if request.method == 'POST':
        feedbackForm = forms.SendFeedback(request.POST)
        if feedbackForm.is_valid():
            feedback = feedbackForm.save(commit=False)
            feedback.user_id = id
            feedback.save()

            user = DefaultUser.objects.get(id=id)
            user.decrypt()

            telegram_msg = 'Sender: ' + user.name + ' ' + user.surname + ' ' + user.patronymic + '\n' + 'Title: ' + feedback.title + '\n' + 'Message: ' + feedback.text + '\n' + 'Mail: ' + user.mail
            SendTelegram(token=GkuSettings.FEEDBACK_TELEGRAM_BOT_KEY, chat_id=GkuSettings.FEEDBACK_TELEGRAM_CHAT_ID, text=telegram_msg)

            return render(request, 'OK/index.html', {'title': 'Спасибо!', 'msg': 'Ваш запрос отправлен на рассмотрение!', 'link': 'account'})
    return HttpResponseRedirect('/account')

def addMohthMeter(requset):
    if 'id' not in requset.session:
        return HttpResponseRedirect('/logout')
    if requset.method == 'POST':
        if 'month' not in requset.POST or 'meters' not in requset.POST:
            return HttpResponseRedirect('/account')
        month = requset.POST['month']
        meters = requset.POST['meters']
