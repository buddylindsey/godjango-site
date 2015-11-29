from django.test import TestCase

import mox
import arrow
from model_mommy import mommy

from newsletter.forms import NewsletterSubscribeForm

from .models import Video
from .views import VideoView, BrowseView, CategoryView
from .mixins import CategoryListMixin


class VideoReviewManagerTest(TestCase):
    def test_published_videos(self):
        mommy.make(Video, publish_date=arrow.now().datetime, _quantity=3)
        mommy.make(Video, _quantity=2)
        videos = Video.objects.published()
        self.assertEqual(3, videos.count())

    def test_premium_videos(self):
        mommy.make(Video, is_premium=True, _quantity=3)
        mommy.make(Video, _quantity=2)
        videos = Video.objects.premium()
        self.assertEqual(3, videos.count())

    def test_not_premium_videos(self):
        mommy.make(Video, _quantity=3)
        videos = Video.objects.not_premium()
        self.assertEqual(3, videos.count())


class VideoModelTest(TestCase):
    def test_video_slugify_on_save(self):
        video = Video()
        video.title = "I am an awesome title"
        video.description = "I am a description"

        video.save()

        self.assertEqual("i-am-an-awesome-title", video.slug)

    def test_model_get_absolute_url(self):
        video = mommy.make('episode.Video', slug='i-is-slug', episode=1)

        self.assertEqual(
            "/{}-i-is-slug/".format(video.episode), video.get_absolute_url())

    def test_model_video_url(self):
        video = Video(title="I is title", description="i is desc")
        video.video_h264 = "h264.mp4"
        video.video_webm = "webm.webm"
        video.save()

        self.assertEqual(
            "/file/?action=play&filename=h264.mp4", video.h264)
        self.assertEqual(
            "/file/?action=play&filename=webm.webm", video.webm)

    def test_length_in_minutes(self):
        video = mommy.make('episode.Video', length=130)

        self.assertEqual(video.length_in_minutes(), '2:10')

    def test_next_video(self):
        video1 = mommy.make(
            'episode.Video', publish_date=arrow.utcnow().datetime, episode=1)
        video2 = mommy.make(
            'episode.Video', publish_date=arrow.utcnow().datetime, episode=2)

        video = video1.next_video()

        self.assertEqual(video, video2)

    def test_no_next_video(self):
        video = mommy.make(
            'episode.Video', publish_date=arrow.utcnow().datetime, episode=1)

        self.assertEqual(None, video.next_video())


class VideoViewTest(TestCase):
    def setUp(self):
        self.view = VideoView()
        self.view.object = None

    def test_attrs(self):
        self.assertEqual(self.view.template_name, 'episode/video.jinja')
        self.assertEqual(self.view.model, Video)
        self.assertEqual(self.view.context_object_name, 'video')

    def test_get_context_data(self):
        self.view.object = mommy.make(Video)
        context = self.view.get_context_data()
        self.assertIsInstance(
            context['newsletter_form'], NewsletterSubscribeForm)

    def test_get_related_videos_non_series(self):
        cat1, cat2 = mommy.make('episode.Category', _quantity=2)
        self.view.object = mommy.make('episode.Video')
        self.view.object.categories.add(cat1)
        self.view.object.categories.add(cat2)

    def test_get_related_videos_with_series(self):
        pass


class BrowseViewTest(TestCase):
    def setUp(self):
        self.view = BrowseView()
        self.view.object_list = {}
        self.mock = mox.Mox()

    def tearDown(self):
        self.mock.UnsetStubs()

    def test_attrs(self):
        self.assertEqual(self.view.model, Video)
        self.assertEqual(self.view.paginate_by, 10)
        self.assertEqual(self.view.context_object_name, 'videos')
        self.assertEqual(self.view.template_name, 'episode/browse.jinja')

    def test_get_context_data(self):
        mommy.make('episode.Video')
        self.mock.StubOutWithMock(CategoryListMixin, 'get_context_data')
        self.mock.StubOutWithMock(BrowseView, 'get_queryset')
        CategoryListMixin.get_context_data().AndReturn({})
        BrowseView.get_queryset().AndReturn(Video.objects.all())

        self.mock.ReplayAll()
        context = self.view.get_context_data()
        self.mock.VerifyAll()

        self.assertEqual(1, context['total_videos'])


class CategoryViewTest(TestCase):
    def setUp(self):
        self.mock = mox.Mox()
        self.view = CategoryView()

    def tearDown(self):
        self.mock.UnsetStubs()

    def test_attrs(self):
        self.assertEqual(self.view.model, Video)
        self.assertEqual(self.view.paginate_by, 10)
        self.assertEqual(self.view.context_object_name, 'videos')
        self.assertEqual(self.view.template_name, 'episode/category.jinja')

    def test_get_context_data(self):
        mommy.make('episode.Video')
        category = mommy.make('episode.Category')
        self.mock.StubOutWithMock(CategoryListMixin, 'get_context_data')
        self.mock.StubOutWithMock(CategoryView, 'get_category')
        self.mock.StubOutWithMock(CategoryView, 'get_queryset')
        CategoryListMixin.get_context_data().AndReturn({})
        CategoryView.get_category().AndReturn(category)
        CategoryView.get_queryset().AndReturn(Video.objects.all())

        self.mock.ReplayAll()
        context = self.view.get_context_data()
        self.mock.VerifyAll()

        self.assertEqual(category, context['category'])
        self.assertEqual(1, context['total_videos'])

    def test_get_category(self):
        category = mommy.make('episode.Category')
        self.view.kwargs = {'slug': category.slug}
        self.assertEqual(category, self.view.get_category())

    def test_get_category_no_category(self):
        self.view.kwargs = {}
        self.assertRaises(AttributeError, self.view.get_category)

    def test_get_queryset(self):
        category = mommy.make('episode.Category')
        video = mommy.make('episode.Video', publish_date=arrow.now().datetime)
        category.videos.add(video)
        self.mock.StubOutWithMock(CategoryView, 'get_category')
        CategoryView.get_category().AndReturn(category)

        self.mock.ReplayAll()
        videos = self.view.get_queryset()
        self.mock.VerifyAll()

        self.assertSequenceEqual(videos, [video])
