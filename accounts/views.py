from django.conf import settings
from django.dispatch import receiver
from django.core.mail import EmailMessage
from django.template import RequestContext
from django.contrib.sites.models import Site
from django.views.generic import TemplateView, FormView
from django.shortcuts import render_to_response, redirect
from django.template.loader import render_to_string
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from episode.models import Favorite
from payments.signals import WEBHOOK_SIGNALS
from payments.settings import INVOICE_FROM_EMAIL
from godjango_cart.forms import CheckoutForm


def logout(request):
    auth_logout(request)
    return redirect('index')


class AccountsContextMixin(object):
    pass


class StripeContenxtMixin(object):
    def get_context_data(self, **kwargs):
        context = super(StripeContenxtMixin, self).get_context_data(**kwargs)
        context['publishable_key'] = settings.STRIPE_PUBLIC_KEY
        return context


class BillingView(AccountsContextMixin, TemplateView):
    template_name = 'accounts/billing.html'


class SettingsView(AccountsContextMixin, TemplateView):
    template_name = 'accounts/settings.html'


class DashboardView(AccountsContextMixin, TemplateView):
    template_name = 'accounts/dashboard.html'


class UpdateBillingView(StripeContenxtMixin, FormView):
    form_class = CheckoutForm
    template_name = 'accounts/update_card.html'
    success_url = '/accounts/billing/'

    def form_valid(self, form):
        token = self.get_form_kwargs().get('data')['stripeToken']

        try:
            self.request.user.customer.update_card(token)
            messages.add_message(
                self.request, messages.SUCCESS,
                'You have successfully updated your card')
        except:
            messages.add_message(
                self.request, messages.ERROR,
                'Something went wrong updating your card, please try again.')

        return super(UpdateBillingView, self).form_valid(form)


@login_required()
def favorites(request):
    favorites = Favorite.objects.filter(user__id=request.user.id)
    return render_to_response(
        'accounts/favorites.html', {'favorites': favorites},
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
