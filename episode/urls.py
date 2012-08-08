from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^(?P<id>\d+)-(?P<slug>[-\w]+)/$', 'episode.views.video', name="episode"),
)
