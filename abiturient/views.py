from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView

from abiturient.models import FAQ, RequiredDocument, SubmitDocument, InfoCard
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
        data = request.POST
        files = request.FILES

        program = None
        program_id = data.get('program')

        if program_id:
            try:
                program = Program.objects.get(id=program_id)
            except Program.DoesNotExist:
                pass

        try:
            submit = SubmitDocument.objects.create(
                # ========= ШАГ 1 =========
                first_name=data.get('first_name'),
                last_name=data.get('last_name'),
                middle_name=data.get('middle_name'),

                phone=data.get('phone'),
                email=data.get('email'),

                birth_date=data.get('birth_date'),
                address=data.get('address'),
                citizenship=data.get('citizenship'),

                # ========= ШАГ 2 =========
                program=program,
                form_of_study=data.get('form_of_study'),
                study_form=data.get('study_form'),
                source=data.get('source'),
                comment=data.get('comment'),

                # ========= ШАГ 3 =========
                passport=files.get('passport'),
                education_document=files.get('education_document'),
                photo=files.get('photo'),
                medical_certificate=files.get('medical_certificate'),
            )

            return JsonResponse({
                'status': 'success',
                'message': 'Заявка успешно отправлена',
                'id': submit.id
            })

        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)



class FAQView(TemplateView):
    template_name = 'otvety-na-voprosy.html'

    def get_context_data(self, **kwargs):
        context = {
            'faqs': FAQ.objects.all()
        }
        return context
