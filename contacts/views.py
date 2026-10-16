from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView

from contacts.forms import ContactRequestForm
from contacts.models import Contacts, Department
from core.utils import form_errors_message


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
        form = ContactRequestForm(request.POST)
        if not form.is_valid():
            return JsonResponse({
                'status': 'error',
                'message': form_errors_message(form),
            }, status=400)

        form.save()
        return JsonResponse({
            'status':  'success',
            'message': 'Ваше сообщение успешно отправлено! Мы свяжемся с вами в течение рабочего дня.'
        })
