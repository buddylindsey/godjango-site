from django.conf.urls import *

urlpatterns = patterns('contact.views',
    url('^', 'feedback', name='feedback'),
)
