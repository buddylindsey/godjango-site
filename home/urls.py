from datetime import datetime

from django.conf.urls import *
from django.views.generic import TemplateView, ListView

from episode.models import Video
from home.rss import LatestVideos

urlpatterns = patterns(
    '',
    url(r'^rss/main', LatestVideos(), name="main_rss"),
    url(r'^$', ListView.as_view(
        model=Video, paginate_by='10', queryset=Video.objects.filter(
            publish_date__lte=datetime.now()).order_by('-publish_date'),
        context_object_name="videos", template_name='home/index.html'),
        name="index"),
    url(
        r'^about/$', TemplateView.as_view(template_name="home/about.html"),
        name="about"),
    url(
        r'^favorite/add/$', 'favorite.views.toggle_favorite',
        name='favorite_toggle'),
)
