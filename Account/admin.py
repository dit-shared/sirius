from django.contrib import admin
from .models import ExtUser, ElectricityMeters, WaterMeters, FeedbackRecord, ElectricityPredictions, WaterPredictions

admin.site.register(ExtUser)
admin.site.register(ElectricityMeters)
admin.site.register(WaterMeters)
admin.site.register(FeedbackRecord)
admin.site.register(ElectricityPredictions)
admin.site.register(WaterPredictions)