from django.conf.urls import patterns, url

from .views import AnalyticsIndexView

urlpatterns = patterns(
    '',
    url(r'^$', AnalyticsIndexView.as_view(), name="analytics"),
)
