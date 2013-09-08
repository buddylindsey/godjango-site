from datetime import datetime
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from contact.forms import FeedbackForm
from episode.models import Video


class FeedbackView(FormView):
    template_name = 'contact/feedback.html'
    form_class = FeedbackForm
    success_url = '/feedback/thankyou/'

    def form_valid(self, form):
        form.send_email()
        return super(FeedbackView, self).form_valid(form)


class ThankyouView(TemplateView):
    template_name = 'contact/thankyou.html'

    def get_context_data(self, **kwargs):
        context = super(ThankyouView, self).get_context_data(**kwargs)
        context['videos'] = Video.objects.filter(
            publish_date__lte=datetime.now()).order_by('-publish_date')
        return context
