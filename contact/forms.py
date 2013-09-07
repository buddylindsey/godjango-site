from django import forms
from django.core.mail import send_mail

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class FeedbackForm(forms.Form):
    email = forms.EmailField(label="Your Email")
    body = forms.CharField(label="Body", widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super(FeedbackForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'

        self.helper.add_input(Submit('submit', 'Submit'))

    def send_email(self):
        send_mail(
            '[GoDjango Feedback Form]', self.cleaned_data['body'],
            self.cleaned_data['email'], ['buddy@buddylindsey.com'],
            fail_silently=False)
