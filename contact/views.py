from django.views.generic.edit import FormView

from contact.forms import FeedbackForm


class FeedbackView(FormView):
    template_name = 'contact/feedback.html'
    form_class = FeedbackForm

    def form_valid(self, form):
        form.send_email()
        return super(FeedbackView, self).form_valid(form)
