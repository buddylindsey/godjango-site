from django.test import TestCase

from model_mommy import mommy
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import (
    TokenAuthentication,
    SessionAuthentication
)
from rest_framework.serializers import ModelSerializer, ValidationError

from episode.models import Video
from newsletter.models import Subscriber
from .views import CreateSubscriber, VideoViewSet
from .serializers import SubscriberSerializer, VideoSerializer


class CreateSubscriberTest(TestCase):
    def setUp(self):
        self.view = CreateSubscriber()

    def test_attrs(self):
        self.assertEqual(self.view.serializer_class, SubscriberSerializer)
        self.assertEqual(self.view.authentication_classes, (SessionAuthentication,))

    def test_perform_create(self):
        pass


class VideoViewSetTest(TestCase):
    def setUp(self):
        self.view = VideoViewSet()

    def test_attrs(self):
        self.assertEqual(self.view.serializer_class, VideoSerializer)
        self.assertEqual(
            self.view.authentication_classes,
            (TokenAuthentication, SessionAuthentication))
        self.assertEqual(self.view.permission_classes, (IsAuthenticated,))


class SubscriberSerializerTest(TestCase):
    def setUp(self):
        self.serializer = SubscriberSerializer()

    def test_attrs(self):
        self.assertEqual(self.serializer.Meta.model, Subscriber)
        self.assertEqual(
            self.serializer.Meta.fields, ('first_name', 'last_name', 'email')
        )

    def test_validate_email_valid(self):
        data = self.serializer.validate_email('data')
        self.assertEqual(data, 'data')

    def test_validate_email_invalid(self):
        mommy.make('newsletter.Subscriber', email='data@data.com', active=True)

        self.assertRaises(ValidationError, self.serializer.validate_email, 'data@data.com')


class VideoSerializerTest(TestCase):
    def setUp(self):
        self.serializer = VideoSerializer()

    def test_attrs(self):
        self.assertEqual(self.serializer.Meta.model, Video)
        self.assertEqual(
            self.serializer.Meta.fields,
            ('pk', 'title', 'description', 'show_notes', 'video_h264',
             'video_webm', 'length', 'episode', 'publish_date', 'is_premium',
             'youtube_id')
        )
