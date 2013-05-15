from django import forms

class CheckoutForm(forms.Form):
    stripeToken = forms.CharField()
