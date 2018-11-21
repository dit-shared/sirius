from django.urls import path
from . import views, accountSettings
from . import meters

urlpatterns = [
    path('', views.index, name='index'),
    path('electricity/', views.electricity, name='electricity'),
    path('water/', views.water, name='water'),
    path('changeMode/', views.changeMode, name='changeMode'),
    path('predictElectricity/', views.predictElectricity, name='predictElectricity'),
    path('predictWater/', views.predictWater, name='predictWater'),
    path('settings/', views.settings, name='settings'),
    path('changeExtendedInfo/', accountSettings.changeExtUserInfo, name='changeExtendedInfo'),
    path('changeStandartInfo/', accountSettings.changeStandartUserInfo, name='changeStandartUserInfo'),
    path('changePassword/', accountSettings.changePassword, name='changePassword'),
    path('feedback/', views.feedback, name='feedback'),
    path('test/', accountSettings.test, name='test')
]