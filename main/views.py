from django.db.models import Prefetch
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from abiturient.models import FAQ
from contacts.models import Contacts
from education.models import Program, ProgramCategory
from main.models import DeadlineDocument, Advantage, NPACategory, \
    CollegeCertificate, Banner, NPADocument
from news.models import News
from people.models import SiteStats, Graduates


class HomeView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        programs = Program.objects.filter(is_active=True).select_related(
            'category')
        stats = SiteStats.objects.first()
        advantage = Advantage.objects.filter(is_active=True)
        npa_cats = NPACategory.objects.prefetch_related(
            Prefetch(
                'documents',
                queryset=NPADocument.objects.filter(is_full=False)
            )
        )
        certificates = CollegeCertificate.objects.filter(is_active=True)
        news = News.objects.filter(is_popular=True)
        graduates = Graduates.objects.order_by('-id')[:4]

        context = {
            'programs': programs,
            'programs_count': programs.filter(is_active=True).count(),
            'categories': ProgramCategory.objects.all(),
            'stats': stats,
            'advantage': advantage,
            'npa_cats': npa_cats,
            'certificates': certificates,
            'news': news,
            'faqs': FAQ.objects.filter(is_popular=True),
            'graduates': graduates,
            'graduates_count': Graduates.objects.count(),
            'banner': Banner.objects.all(),
            'contact': Contacts.objects.first()
        }
        return context

def serve_pdf(request, pk):
    doc = get_object_or_404(NPADocument, pk=pk)
    response = FileResponse(
        doc.file.open('rb'),
        content_type='application/pdf'
    )
    response['Content-Disposition'] = 'inline; filename="{}"'.format(
        doc.file.name)
    response['X-Frame-Options'] = 'SAMEORIGIN'
    return response


class CollegeView(TemplateView):
    template_name = 'college2025-2026.html'

    def get_context_data(self, **kwargs):
        stages = DeadlineDocument.objects.filter(is_active=True)
        programs = Program.objects.filter(is_active=True)

        context = {
            'programs': programs,
            'stages': stages,

        }
        return context



