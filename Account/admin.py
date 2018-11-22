from django.contrib import admin
from .models import ExtUser, ElectricityMeters, WaterMeters, FeedbackRecord

admin.site.register(ExtUser)
admin.site.register(ElectricityMeters)
admin.site.register(WaterMeters)
admin.site.register(FeedbackRecord)