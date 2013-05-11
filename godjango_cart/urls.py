from django.conf.urls import *

urlpatterns = patterns('godjango_cart.views',
        url(r'^add/', 'add', name="add_to_cart"),
        url(r'^remove/', 'remove', name="remove_from_cart"),
        url(r'^checkout/', 'checkout', name="checkout"),
        url(r'^', 'cart', name='cart'),
    )
