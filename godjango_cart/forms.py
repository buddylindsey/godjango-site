from django import forms


class CheckoutForm(forms.Form):
    stripeToken = forms.CharField()
    email = forms.EmailField(required=False)
    plan = forms.CharField()
    coupon = forms.CharField(required=False)
