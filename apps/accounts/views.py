import arrow
import stripe

from django.conf import settings
from django.dispatch import receiver
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse_lazy
from django.contrib.sites.models import Site
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, FormView, CreateView
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import (
    AuthenticationForm, SetPasswordForm, PasswordChangeForm)
from django.contrib import messages

from braces.views import LoginRequiredMixin

from payments.signals import WEBHOOK_SIGNALS
from payments.settings import INVOICE_FROM_EMAIL
from newsletter.models import Subscriber

from .mixins import NextUrlMixin, StripeContenxtMixin, LastAccessMixin
from .forms import (
    CardForm, CancelSubscriptionForm, UserCreateForm, PasswordRecoveryForm)
from .tasks import (
    new_registration_email, password_changed_email, password_reset_email)


def logout(request):
    auth_logout(request)
    return redirect('index')


class LoginView(NextUrlMixin, FormView):
    template_name = 'accounts/login.jinja'
    form_class = AuthenticationForm
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        user = form.get_user()
        auth_login(self.request, user)
        return super(LoginView, self).form_valid(form)

    def form_invalid(self, form):
        messages.add_message(
            self.request, messages.ERROR,
            'Invalid Username or Password. Please Try Again')
        return super(LoginView, self).form_invalid(form)


class AccountRegistrationView(NextUrlMixin, CreateView):
    template_name = 'accounts/register.jinja'
    form_class = UserCreateForm
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        saved_user = form.save()
        user = authenticate(
            username=saved_user.username,
            password=form.cleaned_data['password1'])
        auth_login(self.request, user)

        new_registration_email.delay(user.id)

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        if 'next' in self.request.GET:
            return self.request.GET.get('next')

        return self.success_url


class PasswordRecoveryView(FormView):
    template_name = 'accounts/password_recovery.jinja'
    form_class = PasswordRecoveryForm
    success_url = reverse_lazy('password_recovery')

    def form_valid(self, form):
        user = User.objects.get(email=form.cleaned_data['email'])
        messages.add_message(
            self.request, messages.SUCCESS,
            ('Your password has been reset and emailed to you. '
             'Please check your email'))
        password_reset_email.delay(user.id)
        return super(PasswordRecoveryView, self).form_valid(form)


class BillingView(LoginRequiredMixin, LastAccessMixin, TemplateView):
    template_name = 'accounts/billing.jinja'


class CancelSubscriptionView(LoginRequiredMixin, LastAccessMixin, FormView):
    template_name = 'accounts/cancel.jinja'
    form_class = CancelSubscriptionForm
    success_url = reverse_lazy('billing')

    def form_valid(self, form):
        try:
            self.request.user.customer.cancel()
            messages.add_message(
                self.request, messages.SUCCESS,
                'Your subscription has been cancelled')
        except stripe.StripeError, e:
            messages.add_message(
                self.request, messages.ERROR,
                'Something went wrong: {}'.format(e.message))
        return super(CancelSubscriptionView, self).form_valid(form)


class DashboardView(LoginRequiredMixin, LastAccessMixin, TemplateView):
    template_name = 'accounts/dashboard.jinja'


class SettingsView(LoginRequiredMixin, LastAccessMixin, FormView):
    template_name = 'accounts/settings.jinja'
    success_url = reverse_lazy('settings')

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
        messages.add_message(
            self.request, messages.SUCCESS, 'Your password has been changed')
        password_changed_email.delay(self.request.user.id)
        return super(SettingsView, self).form_valid(form)


class UpdateBillingView(
    LoginRequiredMixin, StripeContenxtMixin, LastAccessMixin, FormView):
    form_class = CardForm
    template_name = 'accounts/update_card.jinja'
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


def card_expired(card):
    expired = arrow.get(
        '{}-{}'.format(card.exp_month, card.exp_year), 'M-YYYY')
    return arrow.utcnow() <= expired


@receiver(WEBHOOK_SIGNALS['charge.failed'])
def card_declined(sender, **kwargs):
    customer = kwargs.get('event').customer

    card = customer.stripe_customer.get('cards').data[0]

    if card_expired(card):
        message_template = 'accounts/email/card_expire_body.txt'
        subject_template = 'accounts/email/card_expire_subject.txt'
    else:
        return

    protocol = getattr(settings, "DEFAULT_HTTP_PROTOCOL", "http")
    site = Site.objects.get_current()
    ctx = {
        "customer": customer,
        "site": site,
        "protocol": protocol,
        "card": card,
    }
    subject = render_to_string(subject_template, ctx)
    subject = subject.strip()
    message = render_to_string(message_template, ctx)
    EmailMessage(
        subject,
        message,
        to=[customer.user.email],
        from_email=INVOICE_FROM_EMAIL
    ).send()


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
