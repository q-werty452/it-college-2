from django.contrib.auth.models import User
from django.contrib.staticfiles import finders
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase


class RichTextEditorTests(TestCase):
    def test_admin_uses_ckeditor5(self):
        self.client.force_login(User.objects.create_superuser('admin', 'a@a.kg', 'x'))
        html = self.client.get('/admin/news/news/add/').content.decode()
        self.assertIn('django_ckeditor_5', html)
        self.assertIn('name="text_ru"', html)
        self.assertNotIn('ckeditor/ckeditor.js', html)
        for path in ['django_ckeditor_5/dist/bundle.js', 'django_ckeditor_5/app.js']:
            if path in html:
                self.assertTrue(finders.find(path), path)

    def test_image_upload_only_for_staff(self):
        upload = SimpleUploadedFile('a.png', b'x', content_type='image/png')
        response = self.client.post('/ckeditor5/image_upload/', {'upload': upload})
        self.assertEqual(response.status_code, 403)
