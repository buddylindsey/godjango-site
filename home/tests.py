from django.test import TestCase
from django.core.urlresolvers import reverse

from home.views import HomeView
from episode.models import Video


class HomeViewTest(TestCase):
    def test_index_page(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(200, response.status_code)

    def test_about_page(self):
        response = self.client.get(reverse("about"))
        self.assertEqual(200, response.status_code)

    def test_feedback_page(self):
        response = self.client.get(reverse("feedback"))
        self.assertEqual(200, response.status_code)

    def test_attrs(self):
        view = HomeView()
        self.assertEqual(view.model, Video)
        self.assertEqual(view.paginate_by, 10)
        self.assertEqual(view.context_object_name, 'videos')
        self.assertEqual(view.template_name, 'home/index.html')
