import arrow

from django.test import TestCase

from model_mommy import mommy

from episode.models import Video
from .views import AboutView, IndexView, PrivacyView


class AboutViewTest(TestCase):
    def setUp(self):
        self.view = AboutView()

    def test_attrs(self):
        self.assertEqual(self.view.template_name, 'home/about.jinja')


class PrivacyViewTest(TestCase):
    def setUp(self):
        self.view = PrivacyView()

    def test_attrs(self):
        self.assertEqual(self.view.template_name, 'home/privacy.jinja')


class IndexViewTest(TestCase):
    def setUp(self):
        self.view = IndexView()

    def test_attrs(self):
        self.assertEqual(self.view.model, Video)
        self.assertEqual(self.view.context_object_name, 'videos')
        self.assertEqual(self.view.template_name, 'home/index.jinja')
        self.assertEqual(self.view.paginate_by, 4)

    def test_get_queryst(self):
        pub1 = arrow.utcnow().replace(days=-1)
        pub2 = pub1.replace(days=-1)
        video1 = mommy.make(
            'episode.Video', id=1, is_premium=True, publish_date=pub1.datetime)
        video2 = mommy.make(
            'episode.Video', id=2, is_premium=True, publish_date=pub2.datetime)
        video3 = mommy.make('episode.Video', id=3)
        qs = self.view.get_queryset()

        self.assertEqual(qs.count(), 2)
        self.assertSequenceEqual(qs, [video1, video2])
