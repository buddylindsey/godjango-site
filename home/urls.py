from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from home.rss import LatestVideos
from home.views import HomeView, CategoryView

urlpatterns = patterns(
    '',
    url(r'^rss/main', LatestVideos(), name="main_rss"),
    url(r'^$', HomeView.as_view(), name="index"),
    url(
        r'^about/$', TemplateView.as_view(template_name="home/about.html"),
        name="about"),
    url(
        r'^category/(?P<slug>[-\w]+)/$', CategoryView.as_view(),
        name='category'),
    url(
        r'^favorite/add/$', 'favorite.views.toggle_favorite',
        name='favorite_toggle'),
)
