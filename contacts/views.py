from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView

from contacts.models import Contacts, Department, ContactForm


class ContactsView(TemplateView):
    template_name = 'kontakty.html'

    def get_context_data(self, **kwargs):
        contact = Contacts.objects.first()
        department = Department.objects.all()

        context = {
            'contact': contact,
            'department': department,
        }
        return context



class ContactFormView(View):
    def get(self, request, *args, **kwargs):
        contact = Contacts.objects.first()
        department = Department.objects.all()
        return render(request, 'kontakty.html', {
            'contact': contact,
            'department': department,
        })

    def post(self, request, *args, **kwargs):
        data = request.POST

        first_name = data.get('first_name')
        last_name = data.get('last_name')
        phone_number = data.get('phone_number')
        email = data.get('email')
        topic = data.get('select', 'other')
        text = data.get('text')

        if not first_name or not last_name or not phone_number or not text:
            return JsonResponse({
                'status': 'error',
                'message': 'Пожалуйста, заполните все обязательные поля.'
            }, status=400)

        try:
            ContactForm.objects.create(
                first_name=first_name,
                last_name=last_name,
                phone_number=phone_number,
                email=email,
                contact_form=topic,
                text=text,
            )

            return JsonResponse({
                'status':  'success',
                'message': 'Ваше сообщение успешно отправлено! Мы свяжемся с вами в течение рабочего дня.'
            })

        except Exception as e:
            return JsonResponse({
                'status':  'error',
                'message': str(e)
            }, status=400)
