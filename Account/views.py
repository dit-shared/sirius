from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect


def index(request):
    if 'id' not in request.session:
        return HttpResponseRedirect('/')
    return render(request, 'FrontPage/index.html')

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
    return render(request, 'AccountSettings/index.html')