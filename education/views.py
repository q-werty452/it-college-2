from django.core.paginator import Paginator
from django.db.models import Q
from django.views.generic import TemplateView

from education.models import TransferInfo, TransferDocument, Program, \
    ProgramCategory, License


class SpecView(TemplateView):
    template_name = 'spec.html'

    def get_context_data(self, **kwargs):
        programs = Program.objects.filter(is_active=True).select_related('category')

        search = self.request.GET.get('search')
        if search:
            programs = programs.filter(
                Q(name__icontains=search) |
                Q(description__icontains=search) |
                Q(study_form__icontains=search)
            )

        category_id = self.request.GET.get('category')
        if category_id and category_id.isdigit():
            programs = programs.filter(category_id=category_id)

        budget = self.request.GET.get('budget')
        if budget == '1':
            programs = programs.filter(has_budget=True)

        sort = self.request.GET.get('sort')
        if sort == 'popular':
            programs = programs.order_by('-is_popular', 'order')

        elif sort == 'duration_asc':
            programs = programs.order_by('duration_years', 'duration_months')

        elif sort == 'duration_desc':
            programs = programs.order_by('-duration_years', '-duration_months')

        elif sort == 'name':
            programs = programs.order_by('name')

        else:
            programs = programs.order_by('order', 'name')

        paginator = Paginator(programs, 10)
        page = self.request.GET.get('page')
        programs = paginator.get_page(page)


        context = {
            'programs': programs,
            'categories': ProgramCategory.objects.all(),
            'licenses': License.objects.all()
        }
        return context

class PriceView(TemplateView):
    template_name = 'stoimost.html'
    def get_context_data(self, **kwargs):
        programs = Program.objects.filter(is_active=True).select_related(
            'category')

        context = {
            'programs': programs,
        }
        return context



class TransferView(TemplateView):
    template_name = 'perevod.html'

    def get_context_data(self, **kwargs):
        info = TransferInfo.objects.first()
        documents = TransferDocument.objects.all()

        context = {
            'info': info,
            'documents': documents,
        }

        return context



class BudgetView(TemplateView):
    template_name = 'budjet-mesta.html'

    def get_context_data(self, **kwargs):
        programs = Program.objects.filter(is_active=True, has_budget=True)

        context = {
            'programs': programs,
            'total_budget': sum(item.benefits_seats for item in programs)
        }
        return context

