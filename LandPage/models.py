from django.db import models
from Gku import crypto
from django.conf import settings
import hashlib, re, random, string
from datetime import datetime
import os

def StandartEncryptField(field, aesKey):
    aes = crypto.AESCipher(aesKey)
    return str(aes.encrypt(field, iv=settings.AES_DEFAULT_IV, random=False), 'utf-8')

def StandartDecryptField(field, aesKey):
    aes = crypto.AESCipher(aesKey)
    return aes.decrypt(field)

def HashPassword(pwd):
    sha256 = hashlib.sha256()
    md5 = hashlib.md5()

    sha256.update(pwd.encode('utf-8'))
    md5.update(pwd.encode('utf-8'))

    return md5.hexdigest()

class DefaultUser(models.Model):
    name = models.CharField(max_length=128, default="")
    surname = models.CharField(max_length=128, default="")
    patronymic = models.CharField(max_length=128, default="")
    login = models.CharField(max_length=128)
    password = models.CharField(max_length=128)
    mail = models.EmailField(max_length=128, blank=True)
    activationKey = models.CharField(max_length=128)
    activationType = models.IntegerField(default=0)
    activationDate = models.DateTimeField(max_length=64, auto_now=True)
    creationDate = models.DateTimeField(max_length=64, auto_now=True)

    def __str__(self):
        return 'User(Name: {0}, Surname : {1}, Patronymic: {2}, Login: {3}, Mail: {4})'.format(
            self.name,
            self.surname,
            self.patronymic,
            self.login,
            self.mail,
        )

    def setCreationDate(self):
        self.creationDate = datetime.now()

    def hashPass(self):
        self.password = HashPassword(self.password)

    def encrypt(self):
        aes = crypto.AESCipher(settings.AES_DEFAULT_KEY)
        if len(self.name) > 0:
            self.name = str(aes.encrypt(self.name), 'utf-8')
        if len(self.surname) > 0:
            self.surname = str(aes.encrypt(self.surname), 'utf-8')
        if len(self.patronymic) > 0:
            self.patronymic = str(aes.encrypt(self.patronymic), 'utf-8')
        self.login = str(aes.encrypt(self.login, iv=settings.AES_DEFAULT_IV, random=False), 'utf-8')
        self.mail = str(aes.encrypt(self.mail, iv=settings.AES_DEFAULT_IV, random=False), 'utf-8')
        self.password = str(aes.encrypt(self.password), 'utf-8')

    def decrypt(self):
        aes = crypto.AESCipher(settings.AES_DEFAULT_KEY)
        if len(self.name) > 0:
            self.name = aes.decrypt(self.name)
        if len(self.surname) > 0:
            self.surname = aes.decrypt(self.surname)
        if len(self.patronymic) > 0:
            self.patronymic = aes.decrypt(self.patronymic)
        self.login = aes.decrypt(self.login)
        self.mail = aes.decrypt(self.mail)
        self.password = aes.decrypt(self.password)

    def chkPass(self):
        if re.match(r'[A-Za-z0-9_\-]{8,}', self.password):
            return True
        return False

    def chkLoginReg(self):
        if re.match(r'[A-Za-z0-9_\-]{8,}', self.login):
            return True
        return False

    def chkMail(self):
        if re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", self.mail):
            return True
        return False

    def genActivationKey(self, type):
        r = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)]) + str(self.id) + str(datetime.now())
        md5 = hashlib.md5()
        md5.update(r.encode('utf-8'))
        self.activationDate = datetime.now()
        self.activationKey = md5.hexdigest()
        self.activationType = type
        return self.activationKey

    def encActivationKey(self, commit=False):
        aes = crypto.AESCipher(settings.AES_ACTIVATION_KEY)
        encKey = str(aes.encrypt(self.activationKey), 'utf-8')
        if commit:
            self.activationKey = encKey
        return encKey

    def decActivationKey(self):
        aes = crypto.AESCipher(settings.AES_ACTIVATION_KEY)
        self.activationKey = str(aes.decrypt(self.activationKey))
        return self.activationKey

    def delActivationKey(self):
        self.activationKey = ""
        self.activationType = 0

    def getEncID(self):
        aes = crypto.AESCipher(settings.AES_ID_KEY)
        return str(aes.encrypt(str(self.id)), 'utf-8')

    @staticmethod
    def chkExistMail(mail):
        if DefaultUser.objects.filter(mail=mail):
            return False
        return True

    @staticmethod
    def chkExistLogin(login):
        if DefaultUser.objects.filter(login=login):
            return False
        return True

class News(models.Model):
    title = models.CharField(max_length=128)
    shortNews = models.CharField(max_length=128)
    detailedNews = models.CharField(max_length=8128)
    creationDate = models.DateTimeField(auto_now=True, max_length=64)
    image = models.ImageField()

    def save(self, *args, **kwargs):
        parts = self.image.name.split('.')
        file_extension = parts[len(parts) - 1]
        self.image.name = 'News_' + self.title + str(random.randint(0, 9999)) + '.' + file_extension
        super(News, self).save(*args, **kwargs)

    def __str__(self):
        return 'News(' + self.title + ' date: ' + str(self.creationDate) + ')'

class Subscriber(models.Model):
    mail = models.EmailField(blank=True, max_length=128)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.mail