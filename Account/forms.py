from django import forms
from LandPage.models import DefaultUser
from .models import WaterMeters, ElectricityMeters, FeedbackRecord, ExtUser
from snowpenguin.django.recaptcha2.fields import ReCaptchaField
from snowpenguin.django.recaptcha2.widgets import ReCaptchaWidget

dateChoices = ((1, 'Январь'),(2,'Февраль'),(3,'Март'),(4,'Апрель'),(5,'Май'), (6,'Июнь'),
               (7, 'Июль'), (8,'Август'), (9,'Сентябрь'), (10,'Октябрь'), (11,'Ноябрь'),
               (12,'Декабрь'))

zoneChoices = ((1, 'ночь'), (2, 'день'), (3, 'пик'), (4, 'полупик'))
yearsChoices = ((2016, 2016), (2017, 2017), (2018, 2018))

class AddElecticityMeter(forms.ModelForm):
    month = forms.ChoiceField(widget=forms.Select, choices=dateChoices)
    year = forms.ChoiceField(widget=forms.Select, choices=yearsChoices)
    valueNight = forms.CharField()
    valueDay = forms.CharField()

    class Meta:
        model = ElectricityMeters
        fields = ('year', 'month', 'valueNight', 'valueDay')

    def __init__(self, *args, **kwargs):
        super(AddElecticityMeter, self).__init__(*args, **kwargs)
        self.fields['month'].widget.attrs.update({'class': 'form-control', })
        self.fields['year'].widget.attrs.update({'class': 'form-control', })
        self.fields['valueNight'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Ночной тариф', })
        self.fields['valueDay'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Дневной тариф', })

class AddWaterMeter(forms.ModelForm):
    month = forms.ChoiceField(widget=forms.Select, choices=dateChoices)
    year = forms.ChoiceField(widget=forms.Select, choices=yearsChoices)
    valueCold = forms.CharField(label='Холодная вода')
    valueHot = forms.CharField(label='Горячая водв')
    class Meta:
        model = WaterMeters
        fields = ('year', 'month', 'valueHot', 'valueCold')

    def __init__(self, *args, **kwargs):
        super(AddWaterMeter, self).__init__(*args, **kwargs)
        self.fields['month'].widget.attrs.update({'class': 'form-control', })
        self.fields['year'].widget.attrs.update({'class': 'form-control', })
        self.fields['valueHot'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Горячая вода', })
        self.fields['valueCold'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Холодная вода', })


class ChangePassword(forms.ModelForm):
    oldpass = forms.CharField(widget=forms.PasswordInput(), label='Старый пароль')
    newpass = forms.CharField(widget=forms.PasswordInput(), label='Пароль')
    repass = forms.CharField(widget=forms.PasswordInput(), label='Повторите пароль')
    class Meta:
        model = DefaultUser
        fields = ('oldpass', 'newpass', 'repass')

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
        fields = ('confirmMail', 'newMail')

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
        fields = ('adress', 'phone', 'ava', 'total_square', 'cnt_fiodr')

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
        fields = ('surname', 'name', 'patronymic')

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
        fields = ('title', 'text')

    def __init__(self, *args, **kwargs):
        super(SendFeedback, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Кратко опишите проблему', })
        self.fields['text'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Дайте развенутое описание проблемы', 'rows': '3'})