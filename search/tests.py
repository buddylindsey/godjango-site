from django.test import TestCase
from django.test.client import RequestFactory

from model_mommy import mommy

from episode.models import Video
from .views import SearchView


class SearchViewTest(TestCase):
    def setUp(self):
        self.view = SearchView()
        self.view.request = RequestFactory()

    def test_attrs(self):
        self.assertEqual(self.view.model, Video)
        self.assertEqual(self.view.context_object_name, 'videos')
        self.assertEqual(self.view.paginate_by, 10)
        self.assertEqual(self.view.template_name, 'home/index.html')

    def test_get_queryset(self):
        mommy.make('episode.Video', description='django')
        mommy.make('episode.Video', title='django')
        mommy.make('episode.Video', show_notes='django')

        self.view.request.GET = {'q': 'django'}
        qs = self.view.get_queryset()

        self.assertEqual(qs.count(), 3)
