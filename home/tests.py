import mox

from django.test import TestCase
from django.views.generic import ListView

from model_mommy import mommy

from .views import AboutView, BrowseView, CategoryView, IndexView
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
        self.assertEqual(self.view.paginate_by, 10)
        self.assertEqual(self.view.context_object_name, 'videos')
        self.assertEqual(self.view.template_name, 'home/index.html')


class BrowseViewTest(TestCase):
    def setUp(self):
        self.view = BrowseView()

    def test_attrs(self):
        self.assertEqual(self.view.model, Video)
        self.assertEqual(self.view.paginate_by, 10)
        self.assertEqual(self.view.context_object_name, 'videos')
        self.assertEqual(self.view.template_name, 'home/index.html')


class CategoryViewTest(TestCase):
    def setUp(self):
        self.view = CategoryView()
        self.mock = mox.Mox()

    def tearDown(self):
        self.mock.UnsetStubs()

    def test_attrs(self):
        self.assertEqual(self.view.model, Video)
        self.assertEqual(self.view.context_object_name, 'videos')
        self.assertEqual(self.view.template_name, 'home/category.html')

    def test_get_context_data(self):
        self.mock.StubOutWithMock(ListView, 'get_context_data')
        self.mock.StubOutWithMock(self.view, 'get_category')

        ListView.get_context_data().AndReturn({})
        self.view.get_category().AndReturn('a category')

        self.mock.ReplayAll()
        context = self.view.get_context_data()
        self.mock.VerifyAll()

        self.assertEqual(context['category'], 'a category')

    def test_get_queryset(self):
        category = mommy.make('episode.Category')
        video = mommy.make('episode.Video', _quantity=3)
        category.videos.add(video[0])

        self.mock.StubOutWithMock(self.view, 'get_category')
        self.view.get_category().AndReturn(category)

        self.mock.ReplayAll()
        qs = self.view.get_queryset()
        self.mock.VerifyAll()

        self.assertEqual(1, qs.count())

    def test_get_category(self):
        mommy.make('episode.Category', title='i are')
        self.view.kwargs = self.mock.CreateMock({})

        self.view.kwargs.get('slug', None).AndReturn('i-are')

        self.mock.ReplayAll()
        cat = self.view.get_category()
        self.mock.VerifyAll()

        self.assertEqual('i-are', cat.slug)

    def test_get_category_no_slug(self):
        mommy.make('episode.Category', title='i are')
        self.view.kwargs = self.mock.CreateMock({})

        self.view.kwargs.get('slug', None).AndReturn(None)

        self.mock.ReplayAll()
        self.assertRaises(AttributeError, self.view.get_category)
        self.mock.VerifyAll()
