from django.views.generic import TemplateView

from events.models import OpenDay, OpenDayFeature


class OpenDayView(TemplateView):
    template_name = 'open-day.html'

    def get_context_data(self, **kwargs):

        context = {
            'open_day': OpenDay.objects.all(),
            'open_day_feature': OpenDayFeature.objects.all()
        }
        return context
