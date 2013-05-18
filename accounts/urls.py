from django.conf.urls import *
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required

from accounts.views import BillingView, SettingsView, DashboardView


urlpatterns = patterns('',
    url(r'', include('social_auth.urls')),
    url(r'^dashboard/$', 
        login_required(DashboardView.as_view()), 
        name="dashboard"
    ),
    url(r'^favorites/$', 'accounts.views.favorites', name="favorites"),
    url(r'^settings/$',
        login_required(SettingsView.as_view()),
        name="settings"),
    url(r'^billing/$',
        login_required(BillingView.as_view()),
        name="billing"
    ),
    url(r'^login/$',
        RedirectView.as_view(url="/accounts/login/github")
    ),
    url(r'^logout/$', auth_logout, name='logout'),

)
