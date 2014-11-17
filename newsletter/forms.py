from django import forms

from .models import Subscriber


class NewsletterSubscribeForm(forms.Form):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    email = forms.EmailField()

    def clean(self):
        cleaned_data = super(NewsletterSubscribeForm, self).clean()

        if Subscriber.objects.filter(
                email=cleaned_data['email'], active=True).exists():
            raise forms.ValidationError('Email address is already subscribed')

        return cleaned_data
