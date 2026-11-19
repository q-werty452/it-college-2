from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from core.views import private_file
from main.views import HomeView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    path('private-files/<path:path>', private_file, name='private-file'),
    path('ckeditor5/', include('django_ckeditor_5.urls')),
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
    path('', include('about.urls')),
    
)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
