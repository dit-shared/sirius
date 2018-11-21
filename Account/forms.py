from django import forms
from LandPage.models import DefaultUser
from .models import WaterMeters, ElectricityMeters, FeedbackRecord, ExtUser
from snowpenguin.django.recaptcha2.fields import ReCaptchaField
from snowpenguin.django.recaptcha2.widgets import ReCaptchaWidget

class AddElecticityMeter(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(), label='Дата')
    zone = forms.IntegerField(widget=forms.ChoiceField(), label='Выберите тариф')
    class Meta:
        model = ElectricityMeters
        fields = {'date', 'value', 'zone'}

class AddWaterMeter(forms.ModelForm):
    date = forms.DateInput()
    value = forms.CharField
    class Meta:
        model = WaterMeters
        fields = {'date', 'value'}

class ChangePassword(forms.ModelForm):
    oldpass = forms.CharField(widget=forms.PasswordInput(), label='Старый пароль')
    newpass = forms.CharField(widget=forms.PasswordInput(), label='Пароль')
    repass = forms.CharField(widget=forms.PasswordInput(), label='Повторите пароль')
    class Meta:
        model = DefaultUser
        fields = {'oldpass', 'newpass', 'repass'}

    def __init__(self, *args, **kwargs):
        super(ChangePassword, self).__init__(*args, **kwargs)
        self.fields['repass'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Повторите пароль', })
        self.fields['newpass'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите новый пароль', })
        self.fields['oldpass'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите старый пароль', })

class ChangeMail(forms.ModelForm):
    newMail = forms.EmailField(label='Новая почта')
    confirmMail = forms.EmailField(label='Повторите почту')
    class Meta:
        model = DefaultUser
        fields = {'confirmMail', 'newMail'}

    def __init__(self, *args, **kwargs):
        super(ChangeMail, self).__init__(*args, **kwargs)
        self.fields['newMail'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите новую почту', })
        self.fields['confirmMail'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Повторите почту', })

class ChangeExtUserInfo(forms.ModelForm):
    adress = forms.CharField(label='Ваше имя', required=False)
    phone = forms.CharField(label='Ваша фамилия', required=False)
    ava = forms.ImageField(label='Аватарка', widget=forms.FileInput(), required=False)
    total_square = forms.IntegerField(label='Площадь помещения', required=False)
    cnt_fiodr = forms.IntegerField(label='Количество проживающих людей', required=False)
    class Meta:
        model = ExtUser
        fields = {'adress', 'phone', 'ava', 'total_square', 'cnt_fiodr'}

    def __init__(self, *args, **kwargs):
        super(ChangeExtUserInfo, self).__init__(*args, **kwargs)
        self.fields['adress'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Ваш адресс', })
        self.fields['phone'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Номер мобильного телефона', })
        self.fields['total_square'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Площадь помещения', })
        self.fields['cnt_fiodr'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Кол-во жителей', })

class ChangeUserInfo(forms.ModelForm):
    name = forms.CharField(label='Ваше имя', required=False)
    surname = forms.CharField(label='Ваша фамилия', required=False)
    patronymic = forms.CharField(label='Ваше отчество', required=False)
    class Meta:
        model = DefaultUser
        fields = {'surname', 'name', 'patronymic'}

    def __init__(self, *args, **kwargs):
        super(ChangeUserInfo, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Ваше имя', })
        self.fields['surname'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Ваша фамилия', })
        self.fields['patronymic'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Ваше отчество', })

class SendFeedback(forms.ModelForm):
    title = forms.CharField(label='Заголовок')
    text = forms.CharField(widget=forms.TextInput)

    class Meta:
        model = FeedbackRecord
        fields = {'title', 'text'}

    def __init__(self, *args, **kwargs):
        super(SendFeedback, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Кратко опишите проблему', })
        self.fields['text'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Дайте развенутое описание проблемы', 'rows': '3'})