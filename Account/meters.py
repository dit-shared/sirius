from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from LandPage.models import DefaultUser
from .models import ExtUser
from Account import forms
import datetime

def addElectricityVal(request):
    if 'id' not in request.session:
        return HttpResponseRedirect('/')
    id = request.session['id']

    if request.method == 'POST':
        addElecValForm = forms.AddElecticityMeter(request.POST)
        if addElecValForm.is_valid():
            meters = addElecValForm.save(commit=False)
            meters.user_id = id
            meters.date = datetime.date(year=int(request.POST['year']), month=int(request.POST['month']))
            meters.save()
            return render(request, 'OK/index.html', {'title': 'ОК', 'msg': 'Показания успешно внесены', 'link': 'account'})
        else:
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
                           'addWaterForm': addWaterForm, 'addElectForm': addElecValForm})
    return HttpResponseRedirect('/account')

def addWaterVal(request):
    if 'id' not in request.session:
        return HttpResponseRedirect('/')
    id = request.session['id']

    if request.method == 'POST':
        addWaterValForm = forms.AddWaterMeter(request.POST)
        if addWaterValForm.is_valid():
            meters = addWaterValForm.save(commit=False)
            meters.user_id = id
            meters.date = datetime.date(year=int(request.POST['year']), month=int(request.POST['month']))
            meters.save()
        else:
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
                           'addWaterForm': addWaterValForm, 'addElectForm': addElecForm})
    return HttpResponseRedirect('/account')
