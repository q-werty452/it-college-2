import io
import shutil
import tempfile

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from PIL import Image

from abiturient.models import SubmitDocument
from education.models import Program, ProgramCategory

MEDIA = tempfile.mkdtemp()


def png(name='photo.png'):
    buf = io.BytesIO()
    Image.new('RGB', (2, 2)).save(buf, 'PNG')
    return SimpleUploadedFile(name, buf.getvalue(), content_type='image/png')


def pdf(name='doc.pdf'):
    return SimpleUploadedFile(name, b'%PDF-1.4', content_type='application/pdf')


@override_settings(MEDIA_ROOT=MEDIA, PRIVATE_MEDIA_ROOT=MEDIA + '/private')
class SubmitDocumentFormTests(TestCase):
    url = '/ru/submit-document/'

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(MEDIA, ignore_errors=True)

    def setUp(self):
        category = ProgramCategory.objects.create(title='IT')
        self.program = Program.objects.create(category=category, name='P', price_per_year=1)

    def data(self, **extra):
        data = {
            'first_name': 'Иван', 'last_name': 'Иванов', 'middle_name': '',
            'phone': '+996555000000', 'email': 'ivan@example.com',
            'birth_date': '2008-01-01', 'address': '', 'citizenship': 'kg',
            'program': self.program.pk, 'form_of_study': 'full_time',
            'study_form': 'budget', 'source': 'site', 'comment': '',
            'passport': pdf(), 'education_document': pdf(), 'photo': png(),
        }
        data.update(extra)
        return data

    def test_valid_application_saved(self):
        response = self.client.post(self.url, self.data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(SubmitDocument.objects.count(), 1)

    def test_required_files(self):
        data = self.data()
        del data['passport'], data['photo']
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(SubmitDocument.objects.count(), 0)

    def test_dangerous_file_types_rejected(self):
        evil = SimpleUploadedFile('evil.html', b'<script>alert(1)</script>')
        response = self.client.post(self.url, self.data(passport=evil))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(SubmitDocument.objects.count(), 0)

    def test_fake_image_rejected(self):
        fake = SimpleUploadedFile('photo.png', b'MZ not an image')
        response = self.client.post(self.url, self.data(photo=fake))
        self.assertEqual(response.status_code, 400)

    def test_invalid_choice_and_date(self):
        response = self.client.post(self.url, self.data(citizenship='zz', birth_date='вчера'))
        self.assertEqual(response.status_code, 400)
        message = response.json()['message']
        self.assertIn('Гражданство', message)
        self.assertIn('Дата рождения', message)
        self.assertNotIn('constraint', message)

    def test_documents_are_private(self):
        import os
        from django.conf import settings
        from django.contrib.auth.models import User

        self.client.post(self.url, self.data())
        application = SubmitDocument.objects.get()
        path = application.passport.path
        self.assertTrue(path.startswith(settings.PRIVATE_MEDIA_ROOT))
        self.assertFalse(os.path.exists(os.path.join(settings.MEDIA_ROOT, application.passport.name)))

        url = application.passport.url
        self.assertTrue(url.startswith('/private-files/'))
        self.assertEqual(self.client.get(f'/media/{application.passport.name}').status_code, 404)

        anonymous = self.client.get(url)
        self.assertEqual(anonymous.status_code, 302)
        self.assertIn('/admin/login/', anonymous['Location'])

        self.client.force_login(User.objects.create_user('user', password='x'))
        self.assertEqual(self.client.get(url).status_code, 302)

        self.client.force_login(User.objects.create_user('staff', password='x', is_staff=True))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['X-Content-Type-Options'], 'nosniff')
        self.assertEqual(self.client.get('/private-files/../db.sqlite3').status_code, 404)
        self.assertEqual(self.client.get('/private-files/documents/nope.pdf').status_code, 404)

    def test_move_applicant_files_command(self):
        import os
        from django.conf import settings
        from django.core.management import call_command

        os.makedirs(os.path.join(settings.MEDIA_ROOT, 'documents'), exist_ok=True)
        for name in ('old.pdf', 'icon.svg'):
            with open(os.path.join(settings.MEDIA_ROOT, 'documents', name), 'wb') as f:
                f.write(b'x')
        application = SubmitDocument.objects.create(
            first_name='a', last_name='b', phone='1', email='a@a.kg', birth_date='2008-01-01',
            citizenship='kg', program=self.program, form_of_study='full_time', study_form='budget',
            passport='documents/old.pdf', education_document='', photo='')

        call_command('move_applicant_files', stdout=open(os.devnull, 'w'))
        self.assertTrue(os.path.exists(os.path.join(settings.PRIVATE_MEDIA_ROOT, 'documents', 'old.pdf')))
        self.assertFalse(os.path.exists(os.path.join(settings.MEDIA_ROOT, 'documents', 'old.pdf')))
        # чужие файлы (иконки документов для поступления) не трогаются
        self.assertTrue(os.path.exists(os.path.join(settings.MEDIA_ROOT, 'documents', 'icon.svg')))
