import mimetypes
import os

from django.contrib.admin.views.decorators import staff_member_required
from django.core.exceptions import SuspiciousFileOperation
from django.http import FileResponse, Http404

from core.storage import PrivateMediaStorage


@staff_member_required
def private_file(request, path):
    storage = PrivateMediaStorage()
    try:
        if not storage.exists(path):
            raise Http404
        file = storage.open(path, 'rb')
    except SuspiciousFileOperation:
        raise Http404

    content_type = mimetypes.guess_type(path)[0] or 'application/octet-stream'
    response = FileResponse(file, content_type=content_type)
    response['Content-Disposition'] = 'inline; filename="{}"'.format(os.path.basename(path))
    response['X-Content-Type-Options'] = 'nosniff'
    response['Content-Security-Policy'] = "default-src 'none'; img-src 'self'; style-src 'unsafe-inline'"
    return response
