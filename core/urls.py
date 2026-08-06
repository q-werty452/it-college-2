from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from main.views import HomeView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
]

urlpatterns += i18n_patterns(
    path('', HomeView.as_view(), name='home-url'),
    path('', include('main.urls')),
    path('', include("contacts.urls")),
    path('', include("news.urls")),
    path('', include("events.urls")),
    path('', include("abiturient.urls")),
    path('', include("education.urls")),
    path('', include("people.urls")),
)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
