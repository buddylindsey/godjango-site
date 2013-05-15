from django.conf.urls import *
from django.views.generic import TemplateView

urlpatterns = patterns('godjango_cart.views',
        url(r'^add/', 'add', name="add_to_cart"),
        url(r'^remove/', 'remove', name="remove_from_cart"),
        url(r'^checkout/', 'checkout', name="checkout"),
        url(r'^confirmation/', 
            TemplateView.as_view(template_name='godjango_cart/confirmation.html'),
            name='order_confirmation'
        ),
        url(r'^', 'cart', name='cart'),
    )
