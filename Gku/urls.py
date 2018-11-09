from django.contrib import admin
from django.conf.urls import include, handler404, handler500
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
import LandPage.views as LandPage_views

urlpatterns = [
    path('', include('LandPage.urls')),
    path('admin/', admin.site.urls),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = LandPage_views.error_404
handler500 = LandPage_views.error_500