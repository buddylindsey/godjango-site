import arrow
import json
import mailchimp

from django.conf import settings
from django.dispatch import receiver
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse_lazy
from django.contrib.sites.models import Site
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import TemplateView, FormView, CreateView
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from django.contrib.auth.forms import (
    AuthenticationForm, SetPasswordForm, PasswordChangeForm)
from django.contrib import messages

from braces.views import LoginRequiredMixin

from payments.signals import WEBHOOK_SIGNALS
from payments.settings import INVOICE_FROM_EMAIL
from godjango_cart.forms import CheckoutForm

from .forms import UserCreateForm, NewsletterSubscribeForm


def logout(request):
    auth_logout(request)
    return redirect('index')


class StripeContenxtMixin(object):
    def get_context_data(self, **kwargs):
        context = super(StripeContenxtMixin, self).get_context_data(**kwargs)
        context['publishable_key'] = settings.STRIPE_PUBLIC_KEY
        return context


class MailchimpMixin(object):
    def get_mailchimp(self):
        return mailchimp.Mailchimp(settings.MAILCHIMP_API_KEY)


class NextUrlMixin(object):
    def get_success_url(self):
        if 'next' in self.request.GET:
            return self.request.GET.get('next')

        return super(NextUrlMixin, self).get_success_url()


class LoginView(NextUrlMixin, FormView):
    template_name = 'accounts/login.html'
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


class AccountRegistrationView(CreateView):
    template_name = 'accounts/register.html'
    form_class = UserCreateForm
    success_url = reverse_lazy('dashboard')

    def get_success_url(self):
        if 'next' in self.request.GET:
            return self.request.GET.get('next')

        return self.success_url

    def form_valid(self, form):
        saved_user = form.save()
        user = authenticate(
            username=saved_user.username,
            password=form.cleaned_data['password1'])
        auth_login(self.request, user)
        return HttpResponseRedirect(self.get_success_url())


class BillingView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/billing.html'


class SettingsView(LoginRequiredMixin, FormView):
    template_name = 'accounts/settings.html'
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


class NewsletterSubscribeView(MailchimpMixin, FormView):
    template_name = 'accounts/subscribe.html'
    form_class = NewsletterSubscribeForm

    def form_valid(self, form):
        try:
            mc = self.get_mailchimp()

            name = {
                'FNAME': form.cleaned_data['first_name'],
                'LNAME': form.cleaned_data['last_name']}
            email = {'email': form.cleaned_data['email']}
            mc.lists.subscribe(
                settings.MAILCHIMP_LIST_MAIN, email, merge_vars=name)
            data = {
                'success': ('Thank you for subscribing. Please confirm '
                            'in the email you that you have subscribed')}
        except mailchimp.ListAlreadySubscribedError:
            data = {'success': 'Thank you. You are already subscribed'}
        except mailchimp.Error, e:
            data = {'errors': {'general': [('Something went horribly wrong. '
                                           'Please try again {}'.format(e))]}}

        if self.request.is_ajax():
            return HttpResponse(json.dumps(data))
        else:
            return super(NewsletterSubscribeForm, self).form_valid(form)

    def form_invalid(self, form):
        if self.request.is_ajax():
            return HttpResponse(json.dumps({"errors": form.errors}))
        else:
            return super(NewsletterSubscribeForm, self).form_invalid(form)


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
