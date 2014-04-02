from django.conf.urls import patterns, url, include
from django.views.generic.base import RedirectView
from django.contrib.auth.decorators import login_required

from accounts.views import (
    FavoriteView, BillingView, SettingsView, DashboardView, UpdateBillingView)


urlpatterns = patterns(
    'accounts.views',
    url(r'', include('social.apps.django_app.urls', namespace='social')),
    url(r'^dashboard/$',
        login_required(DashboardView.as_view()), name="dashboard"),
    url(
        r'^settings/$', login_required(SettingsView.as_view()),
        name="settings"),
    url(
        r'^billing/update_card/$', login_required(UpdateBillingView.as_view()),
        name='update_card'),
    url(
        r'^favorites/$', login_required(FavoriteView.as_view()),
        name="favorites"),
    url(r'^billing/$', login_required(BillingView.as_view()), name="billing"),
    url(r'^login/$', RedirectView.as_view(url="/accounts/login/github")),
    url(r'^logout/$', 'logout', name='logout'),
)
