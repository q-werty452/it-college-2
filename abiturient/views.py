from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView

from abiturient.forms import SubmitDocumentForm
from abiturient.models import FAQ, RequiredDocument, InfoCard
from core.utils import form_errors_message
from education.models import Program
from people.models import SiteStats, Graduates


class AbiturientamView(TemplateView):
    template_name = 'abiturientam.html'

    def get_context_data(self, **kwargs):
        programs = Program.objects.filter(is_active=True)
        stats = SiteStats.objects.first()
        documents = RequiredDocument.objects.all()
        context = {
            'programs': programs,
            'graduates_count': Graduates.objects.count(),
            'faqs': FAQ.objects.filter(is_popular=True),
            'stats': stats,
            'total_budget': sum(item.benefits_seats  for item in programs),
            'documents': documents,

        }
        return context



class SubmitDocumentsView(TemplateView):
    template_name = 'submit-documents.html'



class SubmitDocumentFormView(View):

    def get(self, request, *args, **kwargs):
        programs = Program.objects.filter(is_active=True)

        return render(request, 'submit-documents.html', {
            'programs': programs,
            'info_cards': InfoCard.objects.filter(is_active=True),
        })

    def post(self, request, *args, **kwargs):
        form = SubmitDocumentForm(request.POST, request.FILES)
        if not form.is_valid():
            return JsonResponse({
                'status': 'error',
                'message': form_errors_message(form),
            }, status=400)

        submit = form.save()
        return JsonResponse({
            'status': 'success',
            'message': 'Заявка успешно отправлена',
            'id': submit.id
        })



class FAQView(TemplateView):
    template_name = 'otvety-na-voprosy.html'

    def get_context_data(self, **kwargs):
        context = {
            'faqs': FAQ.objects.all()
        }
        return context
