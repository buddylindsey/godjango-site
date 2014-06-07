from django.conf.urls import patterns, url

from home.rss import LatestVideos
from home.views import AboutView, BrowseView, IndexView, CategoryView

urlpatterns = patterns(
    '',
    url(r'^rss/main', LatestVideos(), name="main_rss"),
    url(r'^$', IndexView.as_view(), name="index"),
    url(r'^browse/$', BrowseView.as_view(), name="browse"),
    url(r'^about/$', AboutView.as_view(), name="about"),
    url(r'^category/(?P<slug>[-\w]+)/$', CategoryView.as_view(),
        name='category'),
    url(r'^favorite/add/$', 'favorite.views.toggle_favorite',
        name='favorite_toggle'),
)
