from django.db import models
import hashlib

class User(models.Model):
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    partonymic = models.CharField(max_length=30)
    login = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    mail = models.CharField(max_length=30)

    def __str__(self):
        return 'User(Name: {0}, Surname : {1}, Partonymic: {2}, Login: {3}, Mail: {4})'.format(
            self.name,
            self.surname,
            self.partonymic,
            self.login,
            self.mail,
        )

    def save(self, *args, **kwargs):
        if not self.pk:
            if User.chkUserLogin(self.login):
                self.hashPass()
                super(User, self).save(args, kwargs)

    def hashPass(self):
        sha256 = hashlib.sha256()
        md5 = hashlib.md5()

        sha256.update(self.password.encode('utf-8'))
        md5.update(self.password.encode('uff-8'))
        self.password = md5.hexdigest()

    @staticmethod
    def chkUserLogin(login):
        if User.objects.filter(login=login):
            return False
        return True
