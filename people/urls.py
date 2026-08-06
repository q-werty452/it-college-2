from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from people.views import DirectorView, GraduatesView, SotrudnikiView

urlpatterns = [
    path('graduates/', GraduatesView.as_view(), name='graduates-url'),
    path('director/', DirectorView.as_view(), name='director-url'),
    path('sotrudniki/', SotrudnikiView.as_view(), name='sotrudniki-url'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)