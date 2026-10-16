from django.test import SimpleTestCase, TestCase

from contacts.models import Contacts
from education.models import Program, ProgramCategory
from main.templatetags.site_extras import phone_digits
from news.models import News, NewsCategory
from people.models import Graduates


class PhoneDigitsTests(SimpleTestCase):
    def test_strips_everything_but_digits(self):
        self.assertEqual(phone_digits('+996 (507) 02-22-02'), '996507022202')
        self.assertEqual(phone_digits(None), '')


class PagesTests(TestCase):
    def setUp(self):
        self.category = ProgramCategory.objects.create(title='IT')
        self.program = Program.objects.create(category=self.category, name='P', price_per_year=1)

    def test_non_numeric_category_ignored(self):
        self.assertEqual(self.client.get('/ru/news/?category=abc').status_code, 200)
        self.assertEqual(self.client.get('/ru/spec/?category=abc').status_code, 200)

    def test_news_page_size(self):
        news_category = NewsCategory.objects.create(title='c')
        for i in range(10):
            News.objects.create(category=news_category, title=f'n{i}', text='t')
        response = self.client.get('/ru/news/')
        self.assertEqual(len(response.context['news']), 9)

    def test_graduates_page_size_and_home_counter(self):
        for i in range(7):
            Graduates.objects.create(name=f'g{i}', release='2024', program=self.program,
                                     short_description='s', full_description='f')
        self.assertEqual(len(self.client.get('/ru/graduates/').context['graduates']), 6)
        self.assertEqual(self.client.get('/ru/').context['graduates_count'], 7)

    def test_contact_phone_links_follow_admin(self):
        Contacts.objects.create(address='a', phone_admission='+996 (700) 11-22-33',
                                phone_students='+996 555 444 333', email='a@a.kg',
                                telegram='t', vkontakte='v', work_hours='9-18')
        html = self.client.get('/ru/contact/').content.decode()
        self.assertIn('href="tel:+996700112233"', html)
        self.assertIn('href="tel:+996555444333"', html)
        self.assertNotIn('tel:+996507022202', html)
