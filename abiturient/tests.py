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


@override_settings(MEDIA_ROOT=MEDIA)
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
