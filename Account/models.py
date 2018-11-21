from django.db import models
from Gku import crypto, settings
import re, random

class ExtUser(models.Model):
    user_id = models.IntegerField(max_length=16)
    adress = models.CharField(max_length=128)
    phone = models.CharField(max_length=128)
    ava = models.ImageField()
    total_square = models.IntegerField(max_length=32)
    cnt_fiodr = models.IntegerField(max_length=32)

    def encrypt(self):
        aes = crypto.AESCipher(settings.AES_DEFAULT_KEY)
        if len(self.adress) > 0:
            self.adress = str(aes.encrypt(self.adress), 'utf-8')
        if len(self.phone) > 0:
            self.phone = str(aes.encrypt(self.phone), 'utf-8')

    def decrypt(self):
        aes = crypto.AESCipher(settings.AES_DEFAULT_KEY)
        if len(self.adress) > 0:
            self.adress = aes.decrypt(self.adress)
        if len(self.phone) > 0:
            self.phone = aes.decrypt(self.phone)

    def chkPhoneNumber(self):
        if re.match(r'^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$', self.phone):
            return True
        return False

    def save(self, *args, **kwargs):
        parts = self.ava.name.split('.')
        file_extension = parts[len(parts) - 1]
        self.ava.name = 'Ava_' + str(self.user_id) + '_' + str(random.randint(0, 9999)) + '.' + file_extension
        super(ExtUser, self).save(*args, **kwargs)

class WaterMeters(models.Model):
    user_id = models.IntegerField(max_length=16)
    date = models.DateField()
    value = models.IntegerField(max_length=16)

class ElectricityMeters(models.Model):
    user_id = models.IntegerField(max_length=16)
    date = models.DateField()
    value = models.IntegerField(max_length=16)
    zone = models.IntegerField(max_length=5)

class FeedbackRecord(models.Model):
    user_id = models.IntegerField(max_length=16)
    title = models.CharField(max_length=64)
    text = models.CharField(max_length=2048)