from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings

def index(request):
    return render(request, 'LandPage/wrapper.html')

def aboutus(request):
    return render(request, 'AboutUs/wrapper.html')

def error_500(request):
    return render(request, '500/error_500.html')

def error_404(request, exception):
    return render(request, '404/error_404.html')