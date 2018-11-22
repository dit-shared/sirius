from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from LandPage.models import DefaultUser
from Account import forms

def addElectricityVal(request):
    if 'id' not in request.session:
        return HttpResponseRedirect('/')
    id = request.session['id']

    if request.method == 'POST':
        addElecValForm = forms.AddElecticityMeter(request.POST)
        if addElecValForm.is_valid():
            meters = addElecValForm.save(commit=False)
            meters.user_id = id
            meters.save()
        else:
            return (request, '')
