from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from LandPage.models import DefaultUser

def addElectricityVal(request):
    if 'id' not in request.session:
        return HttpResponseRedirect('/')
    id = request.session['id']

    if not DefaultUser.objects.filter(id=id).exists():
        return HttpResponseRedirect('/logout')
    return HttpResponse('/OK')