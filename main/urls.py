from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from main.views import HomeView, CollegeView, serve_pdf

urlpatterns = [
    path('college2025-2026/', CollegeView.as_view(), name='college-url'),
    path('npa/pdf/<int:pk>/', serve_pdf, name='npa-pdf'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

