from django.conf.urls import *

urlpatterns = patterns('favorite.ajax',
    url(r'^add/$', 'add_favorite', name='favorite'),
)
