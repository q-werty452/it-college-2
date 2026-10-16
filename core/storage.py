import os

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.utils.deconstruct import deconstructible


@deconstructible
class PrivateMediaStorage(FileSystemStorage):
    """Файлы, которые нельзя отдавать по прямой ссылке (документы абитуриентов).

    Лежат в PRIVATE_MEDIA_ROOT, а не в MEDIA_ROOT, и открываются только
    через core.views.private_file — после входа в админку.
    """

    @property
    def base_location(self):
        return settings.PRIVATE_MEDIA_ROOT

    @property
    def location(self):
        return os.path.abspath(self.base_location)

    @property
    def base_url(self):
        return settings.PRIVATE_MEDIA_URL
