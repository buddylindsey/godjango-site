from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class CardForm(forms.Form):
    stripeToken = forms.CharField()


class CancelSubscriptionForm(forms.Form):
    cancel = forms.BooleanField()


class PasswordRecoveryForm(forms.Form):
    email = forms.EmailField()

    def clean(self):
        try:
            User.objects.get(email=self.cleaned_data['email'])
        except User.DoesNotExist:
            raise forms.ValidationError("Can't find a user based on the email")
        except KeyError:
            raise forms.ValidationError("Email is required")
        return self.cleaned_data


class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True)
    subscribe = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user
