from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from LandPage.models import DefaultUser
from .models import ExtUser, WaterMeters, ElectricityMeters
from Account import forms
import datetime, random

def addElectricityVal(request):
    if 'id' not in request.session:
        return HttpResponseRedirect('/')
    id = request.session['id']

    if request.method == 'POST':
        elecOK = False
        addElecValForm = forms.AddElecticityMeter(request.POST)
        if addElecValForm.is_valid():
            meters = addElecValForm.save(commit=False)
            meters.user_id = id
            meters.date = datetime.date(year=int(request.POST['year']), month=int(request.POST['month']), day=1)
            print(meters.date)

            if ElectricityMeters.objects.filter(user_id=id).filter(date=meters.date).exists():
                ElectricityMeters.objects.filter(user_id=id).filter(date=meters.date).update(valueDay=meters.valueDay)
                ElectricityMeters.objects.filter(user_id=id).filter(date=meters.date).update(valueNight=meters.valueNight)
            else:
                meters.save()

        elecOK = True
        feedbackForm = forms.SendFeedback()
        addWaterForm = forms.AddWaterMeter()

        if not DefaultUser.objects.filter(id=id).exists():
            return HttpResponseRedirect('/logout')

        user = DefaultUser.objects.get(id=id)
        user.decrypt()

        extUser = ExtUser()
        if ExtUser.objects.filter(user_id=id).exists():
            extUser = ExtUser.objects.get(user_id=id)

        return render(request, 'UploadData/index.html',
                      {'user': user, 'extUser': extUser, 'feedbackForm': feedbackForm,
                       'addWaterForm': addWaterForm, 'addElectForm': addElecValForm, 'elecOK': elecOK})
    return HttpResponseRedirect('/account')

def addWaterVal(request):
    if 'id' not in request.session:
        return HttpResponseRedirect('/')
    id = request.session['id']

    if request.method == 'POST':
        waterOK = False
        addWaterValForm = forms.AddWaterMeter(request.POST)
        if addWaterValForm.is_valid():
            meters = addWaterValForm.save(commit=False)
            meters.user_id = id
            meters.date = datetime.date(year=int(request.POST['year']), month=int(request.POST['month']), day=1)

            if WaterMeters.objects.filter(user_id=id).filter(date=meters.date).exists():
                WaterMeters.objects.filter(user_id=id).filter(date=meters.date).update(valueHot=meters.valueHot)
                WaterMeters.objects.filter(user_id=id).filter(date=meters.date).update(valueCold=meters.valueCold)
            else:
                meters.save()

            waterOK = True

        feedbackForm = forms.SendFeedback()
        addElecForm = forms.AddElecticityMeter()

        if not DefaultUser.objects.filter(id=id).exists():
            return HttpResponseRedirect('/logout')

        user = DefaultUser.objects.get(id=id)
        user.decrypt()

        extUser = ExtUser()
        if ExtUser.objects.filter(user_id=id).exists():
            extUser = ExtUser.objects.get(user_id=id)

        return render(request, 'UploadData/index.html',
                      {'user': user, 'extUser': extUser, 'feedbackForm': feedbackForm,
                       'addWaterForm': addWaterValForm, 'addElectForm': addElecForm, 'waterOK': waterOK})
    return HttpResponseRedirect('/account')

def getPredictionsWater(request):
    if 'id' not in request.session:
        return HttpResponseRedirect('/logout')
    id = request.session['id']

    if not DefaultUser.objects.filter(id=id).exists():
        return HttpResponseRedirect('/logout')

    user = DefaultUser.objects.get(id=id)
    user.decrypt()

    extUser = ExtUser()
    if ExtUser.objects.filter(user_id=id).exists():
        extUser = ExtUser.objects.get(user_id=id)

    feedbackForm = forms.SendFeedback()

    coldWater = random.randint(30, 100) / 10
    hotWater = random.randint(30, 100) / 10
    return render(request, 'PredictWater/index.html', {'user': user, 'extUser': extUser, 'feedbackForm': feedbackForm, 'predictions': {'cold': coldWater, 'hot': hotWater}})


def getPredictionsElectricity(request):
    if 'id' not in request.session:
        return HttpResponseRedirect('/logout')
    id = request.session['id']

    if not DefaultUser.objects.filter(id=id).exists():
        return HttpResponseRedirect('/logout')

    user = DefaultUser.objects.get(id=id)
    user.decrypt()

    extUser = ExtUser()
    if ExtUser.objects.filter(user_id=id).exists():
        extUser = ExtUser.objects.get(user_id=id)

    feedbackForm = forms.SendFeedback()

    night = random.randint(300, 1200) / 10
    top = random.randint(300, 1200) / 10
    return render(request, 'PredictElectricity/index.html', {'user': user, 'extUser': extUser, 'feedbackForm': feedbackForm, 'predictions': {'night': night, 'top': top}})