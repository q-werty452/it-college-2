import os
import shutil

from django.conf import settings
from django.core.management.base import BaseCommand

from abiturient.models import SubmitDocument

FILE_FIELDS = ('passport', 'education_document', 'photo', 'medical_certificate')


class Command(BaseCommand):
    help = ('Переносит файлы старых заявок из MEDIA_ROOT в PRIVATE_MEDIA_ROOT. '
            'Трогает только файлы, на которые ссылаются заявки.')

    def handle(self, *args, **options):
        moved = 0
        for application in SubmitDocument.objects.all():
            for field in FILE_FIELDS:
                name = getattr(application, field).name
                if not name:
                    continue
                source = os.path.join(settings.MEDIA_ROOT, name)
                target = os.path.join(settings.PRIVATE_MEDIA_ROOT, name)
                if os.path.exists(source) and not os.path.exists(target):
                    os.makedirs(os.path.dirname(target), exist_ok=True)
                    shutil.move(source, target)
                    moved += 1
        self.stdout.write(self.style.SUCCESS(f'Перенесено файлов: {moved}'))
