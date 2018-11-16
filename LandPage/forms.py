from django import forms
from .models import DefaultUser
from snowpenguin.django.recaptcha2.fields import ReCaptchaField
from snowpenguin.django.recaptcha2.widgets import ReCaptchaWidget

class CreateUser(forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaWidget())
    password = forms.CharField(widget=forms.PasswordInput())
    repass = forms.CharField(widget=forms.PasswordInput())
    mail = forms.EmailField(widget=forms.EmailInput())
    class Meta:
        model = DefaultUser
        fields = ('mail', 'login', 'password', 'repass',)

    def __init__(self, *args, **kwargs):
        super(CreateUser, self).__init__(*args, **kwargs)
        self.fields['mail'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите электронную почту',})
        self.fields['login'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите логин', })
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите пароль', })
        self.fields['repass'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Повторите пароль', })
        self.fields['captcha'].widget.attrs.update({'style':'margin-left: 10%;'})

class Login(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = DefaultUser
        fields = ('login', 'password')

    def __init__(self, *args, **kwargs):
        super(Login, self).__init__(*args, **kwargs)
        self.fields['login'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите логин', })
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите пароль', })

class ForgotPass(forms.ModelForm):
    mail = forms.EmailField(widget=forms.EmailInput())
    captcha = ReCaptchaField(widget=ReCaptchaWidget())

    class Meta:
        model = DefaultUser
        fields = ('mail', )

    def __init__(self, *args, **kwargs):
        super(ForgotPass, self).__init__(*args, **kwargs)
        self.fields['mail'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Ваш логин или пароль', 'style': 'width: 100%; margin-bottom:2%;'})