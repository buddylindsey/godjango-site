from django.test import TestCase

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
