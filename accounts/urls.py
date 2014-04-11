from django.conf.urls import patterns, url, include
from django.views.generic.base import RedirectView

from accounts.views import (
    FavoriteView, BillingView, SettingsView, DashboardView, UpdateBillingView)


urlpatterns = patterns(
    'accounts.views',
    url(r'', include('social.apps.django_app.urls', namespace='social')),
    url(r'^dashboard/$', DashboardView.as_view(), name="dashboard"),
    url(r'^settings/$', SettingsView.as_view(), name="settings"),
    url(
        r'^billing/update_card/$', UpdateBillingView.as_view(),
        name='update_card'),
    url(r'^favorites/$', FavoriteView.as_view(), name="favorites"),
    url(r'^billing/$', BillingView.as_view(), name="billing"),
    url(r'^login/$', RedirectView.as_view(url="/accounts/login/github")),
    url(r'^logout/$', 'logout', name='logout'),
)
