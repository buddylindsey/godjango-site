from django.test import TestCase

from .views import AboutView, IndexView
from episode.models import Video


class AboutViewTest(TestCase):
    def setUp(self):
        self.view = AboutView()

    def test_attrs(self):
        self.assertEqual(self.view.template_name, 'home/about.html')


class IndexViewTest(TestCase):
    def setUp(self):
        self.view = IndexView()

    def test_attrs(self):
        self.assertEqual(self.view.model, Video)
        self.assertEqual(self.view.paginate_by, 8)
        self.assertEqual(self.view.context_object_name, 'videos')
        self.assertEqual(self.view.template_name, 'home/index.jinja')
