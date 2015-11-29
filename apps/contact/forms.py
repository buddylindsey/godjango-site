from django import forms
from django.core.mail import send_mail


class FeedbackForm(forms.Form):
    email = forms.EmailField(label="Your Email")
    body = forms.CharField(label="Body", widget=forms.Textarea)

    def send_email(self):
        send_mail(
            '[GoDjango Feedback Form]', self.cleaned_data['body'],
            self.cleaned_data['email'], ['buddy@buddylindsey.com'],
            fail_silently=False)
