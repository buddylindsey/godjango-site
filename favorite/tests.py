from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from episode.models import Favorite, Video

class TestFavorite(TestCase):
    def _create_user(self):
        return User.objects.create_user('buddy', 'buddy@buddylindsey.com', 'mypass')

    def test_favorite_video_ajax(self):
        user = self._create_user()

        video = Video()
        video.title = "I am a title"
        video.description = "I am description"
        video.save()

        response = self.client.post(reverse('favorite'), {'video_pk': video.id, 'user_pk': user.id}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(200, response.status_code)

        fav = Favorite.objects.all()

        self.assertEqual(user.id, fav[0].user_id)
        self.assertEqual(video.id, fav[0].video_id)
        self.assertEqual("{'success':true}", response.content)

    def test_favorite_video_non_ajax(self):
        user = self._create_user()

        video = Video()
        video.title = "I am a title"
        video.description = "I am description"
        video.save()

        response = self.client.post(reverse('favorite'), {'video_pk': video.id, 'user_pk': user.id})
        self.assertEqual(404, response.status_code)

    def test_favorite_video_ajax_wrong_video(self):
        user = self._create_user()

        video = Video()
        video.title = "I am a title"
        video.description = "I am description"
        video.save()

        response = self.client.post(reverse('favorite'), {'video_pk': 44, 'user_pk': user.id}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(404, response.status_code)

    def test_favorite_video_ajax_wrong_user(self):
        user = self._create_user()

        video = Video()
        video.title = "I am a title"
        video.description = "I am description"
        video.save()

        response = self.client.post(reverse('favorite'), {'video_pk': video.id, 'user_pk': 55}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(404, response.status_code)


