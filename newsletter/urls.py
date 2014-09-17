from django.conf.urls import patterns, url, include

from .views import EmailView, WebhookView

urlpatterns = patterns(
    '',
    url(r'^webhook/$', WebhookView.as_view(), name='mailchimp_webhook'),
    url(r'^email/$', EmailView.as_view(), name='mailchimp_email'),
)
