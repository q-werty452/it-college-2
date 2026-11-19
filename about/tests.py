from io import StringIO

from django.core.management import call_command
from django.test import TestCase


class AboutPageTests(TestCase):
    def test_empty_pages_open(self):
        for lang in ('ru', 'en', 'ky'):
            for url in ('about/', 'about/gallery/'):
                response = self.client.get(f'/{lang}/{url}')
                self.assertEqual(response.status_code, 200, f'/{lang}/{url}')

    def test_seeded_page(self):
        call_command('seed_about', stdout=StringIO())
        response = self.client.get('/ru/about/')
        self.assertContains(response, '<title>О нас — IT COLLEGE</title>', html=False)
        self.assertContains(response, 'Практика с первого курса')
        self.assertContains(response, 'href="/ru/director/"')
