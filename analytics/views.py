from datetime import datetime, timedelta

from django.views.generic import TemplateView
from django.contrib.auth.models import User

import arrow
from braces.views import SuperuserRequiredMixin

from payments.models import CurrentSubscription, Transfer
from newsletter.models import Subscriber


class AnalyticsIndexView(SuperuserRequiredMixin, TemplateView):
    template_name = 'analytics/index.jinja'

    def get_context_data(self, **kwargs):
        context = super(AnalyticsIndexView, self).get_context_data(**kwargs)
        context['active_subscribers'] = self.active_subscribers()
        context['thirty_day_new'] = self.thirty_day_new()
        context['thirty_day_registrations'] = self.thirty_day_registrations()
        context['newsletter_subscribers'] = self.newsletter_subscribers()
        context['total_transfer_this_month'] = self.total_transfer_this_month()
        return context

    def newsletter_subscribers(self):
        return Subscriber.objects.filter(active=True).count()

    def active_subscribers(self):
        return CurrentSubscription.objects.filter(status='active').count() - 5

    def thirty_day_new(self):
        prev_date = datetime.now() - timedelta(days=30)
        return CurrentSubscription.objects.filter(
            start__gte=prev_date, status='active').count()

    def thirty_day_registrations(self):
        final_data = {'labels': range(1,31)[::-1], 'data': []}

        date = arrow.now()
        data = []
        for day in xrange(1, 30):
            date = date.replace(days=-1)
            count = User.objects.filter(
                date_joined__gte=date.floor('day').datetime,
                date_joined__lte=date.ceil('day').datetime).count()
            data.append(count)
        final_data['data'] = data[::-1]
        return final_data

    def total_transfer_this_month(self):
        now = arrow.utcnow()
        transfers = Transfer.objects.filter(
            created_at__gt=now.floor('month').datetime).values_list(
                'amount', flat=True)
        return sum(transfers)
