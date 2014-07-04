from datetime import datetime, timedelta

from django.views.generic import TemplateView
from django.contrib.auth.models import User

import arrow

from payments.models import CurrentSubscription


class AnalyticsIndexView(TemplateView):
    template_name = 'analytics/admin/index.html'

    def get_context_data(self, **kwargs):
        context = super(AnalyticsIndexView, self).get_context_data(**kwargs)
        context['active_subscribers'] = self.active_subscribers()
        context['30_day_new'] = self.thirty_day_new()
        context['30_day_registrations'] = self.thirty_day_registrations()
        return context

    def active_subscribers(self):
        return CurrentSubscription.objects.filter(status='active').count() - 5

    def thirty_day_new(self):
        prev_date = datetime.now() - timedelta(days=30)
        return CurrentSubscription.objects.filter(
            start__gte=prev_date, status='active').count()

    def thirty_day_registrations(self):
        final_data = []

        date = arrow.now()
        for day in xrange(1, 30):
            date = date.replace(days=-1)
            count = User.objects.filter(
                date_joined__gte=date.floor('day').datetime,
                date_joined__lte=date.ceil('day').datetime).count()
            final_data.append(count)

        return final_data
