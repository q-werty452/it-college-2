from django.core.paginator import Paginator
from django.views.generic import TemplateView

from people.models import Director, Graduates, Partner, SiteStats


class GraduatesView(TemplateView):
    template_name = 'graduates-full.html'

    def get_context_data(self, **kwargs):
        graduates_qs = Graduates.objects.order_by('-id')
        stats = SiteStats.objects.first()

        paginator = Paginator(graduates_qs, 6)
        page = self.request.GET.get('page')
        graduates = paginator.get_page(page)


        context = {
            'graduates': graduates,
            'graduates_count': graduates_qs.count(),
            'partners': Partner.objects.all(),
            'stats': stats,
        }
        return context



class DirectorView(TemplateView):
    template_name = 'director.html'

    def get_context_data(self, **kwargs):
        director = Director.objects.first()

        context = {
            'director': director,
        }
        return context


class SotrudnikiView(TemplateView):
    template_name = 'sotrudniki.html'