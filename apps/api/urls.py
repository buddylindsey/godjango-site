from django.conf.urls import patterns, url, include

from rest_framework.routers import DefaultRouter

from .views import CreateSubscriber, VideoViewSet

router = DefaultRouter()

router.register('videos', VideoViewSet, base_name='api_video')

urlpatterns = [
    url(r'^subscriber/create/$',
        CreateSubscriber.as_view(), name='create_subscriber'),
    url(r'^', include(router.urls))
]
