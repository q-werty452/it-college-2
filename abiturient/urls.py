from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from abiturient.views import FAQView, AbiturientamView, SubmitDocumentsView, \
    SubmitDocumentFormView

urlpatterns = [
    path('abiturientam/', AbiturientamView.as_view(), name='abiturientam-url'),
    path('submit-document/', SubmitDocumentFormView.as_view(), name='submit-document-url'),
    path('faqs/', FAQView.as_view(), name='faqs-url'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)