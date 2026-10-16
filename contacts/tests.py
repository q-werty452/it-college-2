from django.test import TestCase

from contacts.models import ContactForm


class ContactFormTests(TestCase):
    url = '/ru/submit-contact-form/'
    data = {'first_name': 'Иван', 'last_name': 'Иванов',
            'phone_number': '+996555000000', 'text': 'Вопрос'}

    def test_email_is_optional(self):
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ContactForm.objects.get().contact_form, 'other')

    def test_invalid_email_rejected(self):
        response = self.client.post(self.url, {**self.data, 'email': 'not-an-email'})
        self.assertEqual(response.status_code, 400)
        self.assertNotIn('constraint', response.json()['message'])

    def test_invalid_topic_rejected(self):
        response = self.client.post(self.url, {**self.data, 'select': 'hacker'})
        self.assertEqual(response.status_code, 400)

    def test_required_fields(self):
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(ContactForm.objects.count(), 0)
