from django.core.paginator import Paginator
from django.utils.translation import gettext as _
from django.views.generic import TemplateView

from people.models import Director, Graduates, Partner, SiteStats, Staff


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

    def get_context_data(self, **kwargs):
        staff = list(Staff.objects.filter(is_active=True).prefetch_related('gallery'))
        leaders = [person for person in staff if person.is_leadership]
        labels = dict(Staff.DEPARTMENT_CHOICES)

        departments = []
        for code, label in Staff.DEPARTMENT_CHOICES:
            members = [p for p in staff if p.department == code and not p.is_leadership]
            if members:
                departments.append({'code': code, 'label': label, 'members': members})

        staff_data = {
            f'staff-{person.pk}': {
                'name': person.full_name,
                'position': person.position,
                'dept': _('Руководство') if person.is_leadership else str(labels[person.department]),
                'photo': person.photo.url if person.photo else '',
                'exp': person.experience,
                'edu': person.education,
                'email': person.email,
                'phone': person.phone,
                'bio': person.bio or person.short_bio,
                'courses': person.course_list,
                'achievements': person.achievement_list,
                'gallery': [item.image.url for item in person.gallery.all()],
            }
            for person in staff
        }

        return {
            'spotlight': leaders[0] if leaders else None,
            'leaders': leaders,
            'departments': departments,
            'staff_data': staff_data,
        }
