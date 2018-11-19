from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('electricity/', views.electricity, name='electricity'),
    path('water/', views.water, name='water'),
    path('changeMode/', views.changeMode, name='changeMode'),
    path('predictElectricity/', views.predictElectricity, name='predictElectricity'),
    path('predictWater/', views.predictWater, name='predictWater'),
    path('settings/', views.settings, name='settings')
]