from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^add/$', 'favorite.ajax.add_favorite', name='favorite'),
)
