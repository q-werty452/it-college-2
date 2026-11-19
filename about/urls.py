from django.urls import path

from .views import AboutView, GalleryView

# Имена 'about-url' и 'gallery-url'. Если у вас уже есть путь/имя для «О нас» —
# просто замените его на AboutView.as_view() в вашем главном urls.py.
urlpatterns = [
    path("about/", AboutView.as_view(), name="about-url"),
    path("about/gallery/", GalleryView.as_view(), name="gallery-url"),
]
