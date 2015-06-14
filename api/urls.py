from django.conf.urls import patterns, url

from .views import CreateSubscriber

urlpatterns = [
    url(r'^subscriber/create/$',
        CreateSubscriber.as_view(), name='create_subscriber'),
]
