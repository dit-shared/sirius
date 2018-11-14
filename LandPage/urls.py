from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('confirmation', views.confirmation, name='confirmation'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('test', views.test, name='test'),
    path('logout', views.logout, name='logout'),
    path('activateAccount', views.activateAccount, name='activateAccount'),
    path('news', views.news, name='news'),
]