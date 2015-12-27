from datetime import datetime, timedelta

from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.db.models import Q

import arrow
from braces.views import SuperuserRequiredMixin

from accounts.models import Profile
from payments.models import CurrentSubscription, Transfer, Charge


class AnalyticsIndexView(SuperuserRequiredMixin, TemplateView):
    template_name = 'analytics/index.jinja'

    def get_context_data(self, **kwargs):
        context = super(AnalyticsIndexView, self).get_context_data(**kwargs)
        context['active_subscribers'] = self.active_subscribers()
        context['thirty_day_new'] = self.thirty_day_new()
        context['thirty_day_registrations'] = self.thirty_day_registrations()
        context['total_transfer_this_month'] = self.total_transfer_this_month()
        context['monthly_subscribers'] = self.monthly_subscribers()
        context['yearly_subscribers'] = self.yearly_subscribers()
        context['active_users'] = self.active_users()
        context['total_charges_this_month'] = self.total_charges_this_month()
        context['total_subscribers_by_amount'] = self.subscribers_by_amount()
        return context

    def active_subscribers(self):
        return CurrentSubscription.objects.filter(status='active').count() - 6

    def monthly_subscribers(self):
        return CurrentSubscription.objects.filter(
            status='active').filter(
                Q(plan='monthly') | Q(plan='monthly-first')).count() - 6

    def yearly_subscribers(self):
        return CurrentSubscription.objects.filter(
            status='active', plan='yearly').count()

    def thirty_day_new(self):
        prev_date = datetime.now() - timedelta(days=30)
        return CurrentSubscription.objects.filter(
            start__gte=prev_date, status='active').count()

    def thirty_day_registrations(self):
        final_data = {'labels': range(1, 31)[::-1], 'data': []}

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

    def active_users(self):
        today = arrow.utcnow()
        return Profile.objects.filter(
            last_access__gte=today.floor('day').datetime).count()

    def total_charges_this_month(self):
        now = arrow.utcnow()
        transfers = Transfer.objects.filter(
            created_at__gt=now.floor('month').datetime).values_list(
                'charge_gross', flat=True)
        return sum(transfers)

    def subscribers_by_amount(self):
        amounts = CurrentSubscription.objects.filter(
            status='active').distinct().values_list('amount', flat=True)

        return [
            {a: CurrentSubscription.objects.filter(
                status='active', amount=a).count()} for a in sorted(amounts)]
