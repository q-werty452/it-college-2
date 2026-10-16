import json

from django.test import TestCase

from people.models import Staff


class StaffPageTests(TestCase):
    url = '/ru/sotrudniki/'

    def test_empty_page(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Информация о сотрудниках скоро появится')
        self.assertNotContains(response, 'randomuser.me')

    def test_staff_from_admin(self):
        director = Staff.objects.create(
            full_name='Директоров Д. Д.', position='Директор', is_leadership=True,
            phone='+996 (312) 12-34-56', email='dir@example.com', tags='Канд. наук, Методист',
            achievements='Первое\n\nВторое\n', order=1)
        teacher = Staff.objects.create(full_name='Учителев У. У.', position='Преподаватель',
                                       department='it', courses='Python\nDjango')
        Staff.objects.create(full_name='Скрытый', position='x', is_active=False)

        response = self.client.get(self.url)
        self.assertEqual(response.context['spotlight'], director)
        self.assertEqual(response.context['leaders'], [director])
        self.assertEqual([d['code'] for d in response.context['departments']], ['it'])
        self.assertContains(response, 'href="tel:+996312123456"')
        self.assertNotContains(response, 'Скрытый')

        html = response.content.decode()
        start = html.index('<script id="staff-data" type="application/json">') + len('<script id="staff-data" type="application/json">')
        data = json.loads(html[start:html.index('</script>', start)])
        self.assertEqual(data[f'staff-{director.pk}']['achievements'], ['Первое', 'Второе'])
        self.assertEqual(data[f'staff-{teacher.pk}']['courses'], ['Python', 'Django'])
        self.assertEqual(data[f'staff-{teacher.pk}']['dept'], 'ИТ-кафедра')
