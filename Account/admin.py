from django.contrib import admin
from .models import ExtUser, ElectricityMeters, WaterMeters

admin.site.register(ExtUser)
admin.site.register(ElectricityMeters)
admin.site.register(WaterMeters)