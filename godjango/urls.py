from django.contrib import admin
from django.views.generic import DetailView
from django.conf.urls import patterns, include, url

from episode.models import Video

admin.autodiscover()

urlpatterns = patterns('',
    # Admin
    url(r'^admin/', include(admin.site.urls)),

    # Home
    url(r'^', include('home.urls')),

    # Accounts
    url('^accounts/', include('accounts.urls')),    

    # Episodes
    url(r'^favorite/', include('favorite.urls'), name="favorite"),
    url(r'^(?P<pk>\d+)-(?P<slug>[-\w]+)/$', DetailView.as_view(
            model=Video,
            template_name="episode/video.html"
        ), name="episode"),

)
