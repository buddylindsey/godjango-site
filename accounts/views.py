from django.conf import settings
from django.dispatch import receiver
from django.core.mail import EmailMessage
from django.template import RequestContext
from django.contrib.sites.models import Site
from django.views.generic import TemplateView
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required

from episode.models import Favorite
from payments.signals import WEBHOOK_SIGNALS
from payments.settings import INVOICE_FROM_EMAIL

def logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/')

class AccountsContextMixin(object):
    pass

class BillingView(AccountsContextMixin, TemplateView):
    template_name = 'accounts/billing.html'

class SettingsView(AccountsContextMixin, TemplateView):
    template_name = 'accounts/settings.html'

class DashboardView(AccountsContextMixin, TemplateView):
    template_name = 'accounts/dashboard.html'

@login_required()
def favorites(request):
    favorites = Favorite.objects.filter(user__id=request.user.id)
    return render_to_response('accounts/favorites.html',
        { 'favorites': favorites},
        context_instance=RequestContext(request))

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



