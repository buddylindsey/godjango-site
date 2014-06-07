from django.contrib import admin
from django.conf.urls import patterns

from .views import AnalyticsIndexView

admin_urls = patterns(
    '',
    (r'^analytics/$', admin.site.admin_view(AnalyticsIndexView.as_view()))
)
