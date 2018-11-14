from django.contrib import admin
from .models import DefaultUser, News

admin.site.register(DefaultUser)
admin.site.register(News)
