from django.urls import path
from core import settings
from django.conf.urls.static import static

from events.views import OpenDayView

urlpatterns = [
    path('open-day/', OpenDayView.as_view(), name='open-day-url' ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)