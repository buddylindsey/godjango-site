from django.conf.urls import patterns, url, include

from accounts.views import (
    AccountRegistrationView, BillingView, CancelSubscriptionView,
    DashboardView, LoginView, PasswordRecoveryView, SettingsView,
    UpdateBillingView)


urlpatterns = patterns(
    'accounts.views',
    url(r'', include('social.apps.django_app.urls', namespace='social')),
    url(r'^register/$', AccountRegistrationView.as_view(), name='register'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', 'logout', name='logout'),
    url(r'^password_recovery/$', PasswordRecoveryView.as_view(),
        name='password_recovery'),

    url(r'^dashboard/$', DashboardView.as_view(), name="dashboard"),
    url(r'^settings/$', SettingsView.as_view(), name="settings"),
    url(r'^billing/update_card/$', UpdateBillingView.as_view(),
        name='update_card'),
    url(r'^billing/$', BillingView.as_view(), name="billing"),
    url(r'^cancel/$', CancelSubscriptionView.as_view(),
        name="cancel_subscription"),
)
