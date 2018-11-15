from django import forms
from .models import DefaultUser
from snowpenguin.django.recaptcha2.fields import ReCaptchaField
from snowpenguin.django.recaptcha2.widgets import ReCaptchaWidget

class CreateUser(forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaWidget())
    class Meta:
        model = DefaultUser
        fields = ('mail', 'login', 'password')

class Login(forms.ModelForm):
    class Meta:
        model = DefaultUser
        fields = ('login', 'password')
