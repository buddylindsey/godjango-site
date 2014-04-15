from django.conf import settings
from django.dispatch import receiver
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse_lazy
from django.contrib.sites.models import Site
from django.views.generic import TemplateView, FormView, CreateView
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import (
    AuthenticationForm, SetPasswordForm, PasswordChangeForm)
from django.contrib import messages

from braces.views import LoginRequiredMixin

from payments.signals import WEBHOOK_SIGNALS
from payments.settings import INVOICE_FROM_EMAIL
from godjango_cart.forms import CheckoutForm

from .forms import UserCreateForm


def logout(request):
    auth_logout(request)
    return redirect('index')


class StripeContenxtMixin(object):
    def get_context_data(self, **kwargs):
        context = super(StripeContenxtMixin, self).get_context_data(**kwargs)
        context['publishable_key'] = settings.STRIPE_PUBLIC_KEY
        return context


class LoginView(FormView):
    template_name = 'accounts/login.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('dashboard')

    def get_success_url(self):
        if 'next' in self.request.GET:
            return self.request.GET.get('next')

        return super(LoginView, self).get_success_url()

    def form_valid(self, form):
        user = form.get_user()
        auth_login(self.request, user)
        return super(LoginView, self).form_valid(form)

    def form_invalid(self, form):
        messages.add_message(
            self.request, messages.ERROR,
            'Invalid Username or Password. Please Try Again')
        return super(LoginView, self).form_invalid(form)


class AccountRegistrationView(CreateView):
    template_name = 'accounts/register.html'
    form_class = UserCreateForm
    success_url = reverse_lazy('dashboard')


class BillingView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/billing.html'


class SettingsView(LoginRequiredMixin, FormView):
    template_name = 'accounts/settings.html'

    def get_form_kwargs(self):
        kwargs = super(SettingsView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_form_class(self):
        if self.request.user.has_usable_password():
            return PasswordChangeForm
        else:
            return SetPasswordForm

    def form_valid(self, form):
        form.save()
        return super(SettingsView, self).form_valid(form)


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/dashboard.html'


class UpdateBillingView(LoginRequiredMixin, StripeContenxtMixin, FormView):
    form_class = CheckoutForm
    template_name = 'accounts/update_card.html'
    success_url = reverse_lazy('billing')

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


class FavoriteView(LoginRequiredMixin, TemplateView):
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
