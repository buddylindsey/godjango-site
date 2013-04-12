from django.conf.urls import *
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView
from django.contrib.auth import logout as auth_logout


urlpatterns = patterns('',
    url(r'', include('social_auth.urls')),
    url(r'^dashboard/$', 'accounts.views.dashboard', name="dashboard"),
    url(r'^favorites/$', 'accounts.views.favorites', name="favorites"),
    url(r'^settings/$', 'accounts.views.settings', name="settings"),
    url(r'^billing/$', 'accounts.views.billing', name="billing"),
    url(r'^login/$', RedirectView.as_view(url="/accounts/login/github")),
    url(r'^logout/$', auth_logout, name='logout'),

)
