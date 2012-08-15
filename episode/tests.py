from django.test import TestCase
from django.conf import settings
from django.utils.timezone import now

from models import Video

class VideoModelTest(TestCase): 
    def test_model_fields(self):
        video = Video()
        video.title = "The Title"
        video.slug = "the-title"
        video.thumbnail_image = "thumbnail.jpg"
        video.preview_image = "preview.jpg"
        video.description = "long description here"
        video.show_notes = "show notes here"
        video.video_h264 = "video.mp4"
        video.video_webm = "video.webm"
        video.length = 12
        video.episode = 1
        video.publish_date = now()
        #video.is_premium = False
        #video.price = 105.00

        video.save()
        self.assertEqual(video, Video.objects.get(title__exact="The Title")) 
    
    def test_video_slugify_on_save(self):
        video = Video()
        video.title = "I am an awesome title"
        video.description = "I am a description"

        video.save()

        self.assertEqual("i-am-an-awesome-title", video.slug)

    def test_model_get_absolute_url(self):
        video = Video(title="I is title",description="i is desc")
        video.save()

        self.assertEqual("/%s-%s/" % (video.id, video.slug), video.get_absolute_url())

    def test_model_video_url(self):
        video = Video(title="I is title",description="i is desc")
        video.video_h264 = "h264.mp4"
        video.video_webm = "webm.webm"
        video.save()
        
        self.assertEqual("/episode%s/%s" % (video.id, "h264.mp4"), video.h264)
        self.assertEqual("/episode%s/%s" % (video.id, "webm.webm"), video.webm)
