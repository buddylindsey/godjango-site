from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from godjango_cart.views import (
    CartView, CartAddView, CartRemoveView, CheckoutView)

urlpatterns = patterns(
    'godjango_cart.views',
    url(r'^add/', CartAddView.as_view(), name="add_to_cart"),
    url(r'^remove/', CartRemoveView.as_view(), name="remove_from_cart"),
    url(r'^checkout/', CheckoutView.as_view(), name="checkout"),
    url(
        r'^confirmation/',
        TemplateView.as_view(template_name='godjango_cart/confirmation.html'),
        name='order_confirmation'
    ),
    url(r'^', CartView.as_view(), name='cart'),
)
