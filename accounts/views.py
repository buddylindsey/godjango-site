from django.conf import settings
from django.dispatch import receiver
from django.core.mail import EmailMessage
from django.contrib.sites.models import Site
from django.views.generic import TemplateView
from django.shortcuts import render_to_response, redirect
from django.template.loader import render_to_string
from django.contrib.auth import logout as auth_logout

from payments.signals import WEBHOOK_SIGNALS
from payments.settings import INVOICE_FROM_EMAIL


def logout(request):
    auth_logout(request)
    return redirect('index')


class AccountsContextMixin(object):
    pass


class BillingView(AccountsContextMixin, TemplateView):
    template_name = 'accounts/billing.html'


class SettingsView(AccountsContextMixin, TemplateView):
    template_name = 'accounts/settings.html'


class DashboardView(AccountsContextMixin, TemplateView):
    template_name = 'accounts/dashboard.html'


class FavoriteView(AccountsContextMixin, TemplateView):
    template_name = 'accounts/favorites.html'


@receiver(WEBHOOK_SIGNALS['customer.subscription.deleted'])
def subscription_udpated(sender, **kwargs):
    customer = kwargs.get('event').customer
    site = Site.objects.get_current()
    protocol = getattr(settings, "DEFAULT_HTTP_PROTOCOL", "http")
    ctx = {
        "customer": customer,
        "site": site,
        "protocol": protocol,
    }
    subject = render_to_string("accounts/email/unsubscribe_subject.txt", ctx)
    subject = subject.strip()
    message = render_to_string("accounts/email/unsubscribe_body.txt", ctx)
    EmailMessage(
        subject,
        message,
        to=[customer.user.email],
        from_email=INVOICE_FROM_EMAIL
    ).send()
