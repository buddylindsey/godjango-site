from datetime import datetime, timedelta

from django.views.generic import TemplateView

from payments.models import CurrentSubscription


class AnalyticsIndexView(TemplateView):
    template_name = 'analytics/admin/index.html'

    def get_context_data(self, **kwargs):
        context = super(AnalyticsIndexView, self).get_context_data(**kwargs)
        context['active_subscribers'] = CurrentSubscription.objects.count() - 6
        context['30_day_new'] = self.thirty_day_new()
        return context

    def thirty_day_new(self):
        prev_date = datetime.now() - timedelta(days=30)
        return CurrentSubscription.objects.filter(start__gte=prev_date).count()
