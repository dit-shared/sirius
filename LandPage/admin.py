from django.contrib import admin
from .models import DefaultUser, News, Subscriber

admin.site.register(DefaultUser)
admin.site.register(News)
admin.site.register(Subscriber)
