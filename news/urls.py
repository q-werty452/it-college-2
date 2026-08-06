from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from news.views import NewsView, NewsDetailView

urlpatterns = [
    path('news/', NewsView.as_view(), name='news-url' ),
    path('news/<int:pk>/', NewsDetailView.as_view(), name='news-detail-url' ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)