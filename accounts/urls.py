from django.conf.urls import patterns, url, include

from accounts.views import (
    AccountRegistrationView, BillingView,  DashboardView, FavoriteView,
    LoginView, SettingsView, UpdateBillingView, NewsletterSubscribeView)


urlpatterns = patterns(
    'accounts.views',
    url(r'', include('social.apps.django_app.urls', namespace='social')),
    url(r'^register/$', AccountRegistrationView.as_view(), name='register'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', 'logout', name='logout'),

    url(r'^dashboard/$', DashboardView.as_view(), name="dashboard"),
    url(r'^settings/$', SettingsView.as_view(), name="settings"),
    url(
        r'^billing/update_card/$', UpdateBillingView.as_view(),
        name='update_card'),
    url(r'^favorites/$', FavoriteView.as_view(), name="favorites"),
    url(r'^billing/$', BillingView.as_view(), name="billing"),
    url(r'^newsletter-subscribe/$',
        NewsletterSubscribeView.as_view(), name='newsletter-subscribe')
)
