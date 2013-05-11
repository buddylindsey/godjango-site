from django.test import TestCase
from django.core.urlresolvers import reverse

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
