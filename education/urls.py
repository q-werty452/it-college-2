from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from education.views import TransferView, SpecView, PriceView, BudgetView

urlpatterns = [
    path('spec/', SpecView.as_view(), name='spec-url'),
    path('stoimost/', PriceView.as_view(), name='stoimost-url'),
    path('perevod/', TransferView.as_view(), name='perevod-url'),
    path('budjet/', BudgetView.as_view(), name='budget-url'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)