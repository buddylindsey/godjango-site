from django.conf.urls import *

urlpatterns = patterns('',
    url(r'^add/$', 'favorite.ajax.add_favorite', name='favorite'),
)
