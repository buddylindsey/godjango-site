from django.conf.urls import patterns, url

from home.rss import LatestVideos, AllContent
from home.views import AboutView, IndexView, PrivacyView

urlpatterns = patterns(
    '',
    url(r'^rss/main', LatestVideos(), name="main_rss"),
    url(r'^rss/all', AllContent(), name="all_rss"),
    url(r'^$', IndexView.as_view(), name="index"),
    url(r'^about/$', AboutView.as_view(), name="about"),
    url(r'^privacy/$', PrivacyView.as_view(), name="privacy"),
)
