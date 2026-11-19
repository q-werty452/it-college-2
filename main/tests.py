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


class AdminTests(TestCase):
    def setUp(self):
        from django.contrib.auth.models import User
        self.client.force_login(User.objects.create_superuser('admin', 'a@a.kg', 'x'))

    def test_every_admin_page_opens(self):
        from django.contrib import admin
        from django.urls import reverse
        for model in admin.site._registry:
            info = (model._meta.app_label, model._meta.model_name)
            # страница «О нас» из списка сразу ведёт на форму редактирования
            response = self.client.get(reverse('admin:%s_%s_changelist' % info), follow=True)
            self.assertEqual(response.status_code, 200, model)

    def test_singletons_allow_only_one_record(self):
        from people.models import SiteStats
        url = '/admin/people/sitestats/add/'
        self.assertEqual(self.client.get(url).status_code, 200)
        SiteStats.objects.create()
        self.assertEqual(self.client.get(url).status_code, 403)

    def test_submissions_are_read_only_except_status(self):
        from contacts.models import ContactForm
        request = ContactForm.objects.create(first_name='И', last_name='И', phone_number='1', text='t')
        self.assertEqual(self.client.get('/admin/contacts/contactform/add/').status_code, 403)
        page = self.client.get(f'/admin/contacts/contactform/{request.pk}/change/').content.decode()
        self.assertIn('name="status"', page)
        self.assertNotIn('name="text"', page)


class PageHeroTests(TestCase):
    def test_default_and_admin_hero(self):
        from main.models import PageHero
        self.assertContains(self.client.get('/ru/news/'), '<h1>Новости</h1>')
        PageHero.objects.create(page='news', title_ru='События колледжа', subtitle_ru='Строка 1\nСтрока 2')
        response = self.client.get('/ru/news/')
        self.assertContains(response, '<h1>События колледжа</h1>')
        self.assertContains(response, 'Строка 1<br>Строка 2')

    def test_every_hero_page_renders(self):
        for url in ['abiturientam/', 'news/', 'budjet/', 'college2025-2026/', 'director/',
                    'contact/', 'open-day/', 'faqs/', 'perevod/', 'sotrudniki/', 'spec/',
                    'stoimost/', 'submit-document/', 'graduates/']:
            for lang in ['ru', 'en', 'ky']:
                self.assertEqual(self.client.get(f'/{lang}/{url}').status_code, 200, url)


class NewsDetailTests(TestCase):
    def test_title_html_and_gallery(self):
        category = NewsCategory.objects.create(title='c')
        news = News.objects.create(category=category, title='Моя новость', text='<p><b>жирный</b></p>')
        response = self.client.get(f'/ru/news/{news.pk}/')
        self.assertContains(response, '<h1>Моя новость</h1>')
        self.assertContains(response, '<b>жирный</b>')
        self.assertNotContains(response, 'кибербезопасности')
