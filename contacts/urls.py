from django.urls import path
from core import settings
from django.conf.urls.static import static

from contacts.views import ContactsView, ContactFormView

urlpatterns = [
    path('contact/', ContactsView.as_view(), name='contact-url' ),
    path('submit-contact-form/', ContactFormView.as_view(), name='submit-contact-url'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)