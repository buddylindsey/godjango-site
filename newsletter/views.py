import json

from django.http import HttpResponse
from django.views.generic import View, FormView

from braces.views import CsrfExemptMixin

from .mixins import MailchimpMixin
from .forms import NewsletterSubscribeForm
from .models import Event, Subscriber
from .tasks import newsletter_subscribe


class WebhookView(CsrfExemptMixin, View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("data")

    def post(self, request, *args, **kwargs):
        event = Event.objects.create(
            data=request.POST, kind=request.POST['type'])
        event.process()
        return HttpResponse()


class EmailView(View):
    def form_valid(self, form):
        subscriber = Subscriber.objects.create(
            first_name=form.cleaned_data['first_name'],
            last_name=form.cleaned_data['last_name'],
            email=form.cleaned_data['email'])
        newsletter_subscribe.delay(**form.cleaned_data)

        final_data = {
            'id': subscriber.id, 'first_name': subscriber.first_name,
            'last_name': subscriber.last_name, 'email': subscriber.email}

        return HttpResponse(
            json.dumps(final_data), content_type="application/json")

    def form_invalid(self, form):
        final_data = {'errors': form.errors}
        return HttpResponse(
            json.dumps(final_data), content_type="application/json",
            status=422)

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)

        form = NewsletterSubscribeForm(data)

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class NewsletterSubscribeView(MailchimpMixin, FormView):
    template_name = 'accounts/subscribe.html'
    form_class = NewsletterSubscribeForm

    def form_valid(self, form):
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        email = form.cleaned_data['email']
        self.newsletter_subscribe(first_name, last_name, email)

        if self.request.is_ajax():
            return HttpResponse(
                json.dumps({'success': 'Thank you for subscribing'}))
        else:
            return super(NewsletterSubscribeForm, self).form_valid(form)

    def form_invalid(self, form):
        if self.request.is_ajax():
            return HttpResponse(json.dumps({"errors": form.errors}))
        else:
            return super(NewsletterSubscribeForm, self).form_invalid(form)
