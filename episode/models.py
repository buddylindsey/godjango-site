from datetime import datetime, timedelta

from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

import arrow
from mistune import Markdown
from djblog.utils import SyntaxHighlightRenderer

from django_extensions.db.models import (
    TimeStampedModel, TitleSlugDescriptionModel)
from django.utils.encoding import python_2_unicode_compatible


class VideoQuerySet(models.query.QuerySet):
    def published(self):
        return self.filter(
            publish_date__lte=arrow.now().datetime).order_by('-publish_date')

    def premium(self):
        return self.filter(is_premium=True)

    def not_premium(self):
        return self.filter(is_premium=False)


class VideoManager(models.Manager):
    def published(self):
        return self.get_query_set().published()

    def premium(self):
        return self.get_query_set().premium()

    def not_premium(self):
        return self.get_query_set().not_premium()

    def get_query_set(self):
        return VideoQuerySet(self.model, using=self._db)


@python_2_unicode_compatible
class Video(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True)
    thumbnail_image = models.CharField(max_length=200, null=True, blank=True)
    preview_image = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField()
    show_notes = models.TextField(null=True, blank=True)
    transcript = models.TextField(null=True, blank=True)
    video_h264 = models.CharField(max_length=1000, null=True, blank=True)
    video_webm = models.CharField(max_length=1000, null=True, blank=True)
    length = models.PositiveIntegerField(null=True, blank=True)
    episode = models.PositiveIntegerField(null=True, blank=True)
    publish_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    favorites = models.ManyToManyField(
        User, blank=True, related_name='favorites')
    is_premium = models.BooleanField(default=False)
    price = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True)
    meta_keywords = models.TextField(null=True, blank=True)
    widescreen = models.BooleanField(default=False)

    objects = VideoManager()

    def get_absolute_url(self):
        return reverse('episode', kwargs={'pk': self.id, 'slug': self.slug})

    def _h264(self):
        return "/file/?action=play&filename={}".format(self.video_h264)
    h264 = property(_h264)

    def _webm(self):
        return "/file/?action=play&filename={}".format(self.video_webm)
    webm = property(_webm)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Video, self).save(*args, **kwargs)

    def h264_download(self):
        return "/file/?filename={}".format(self.video_h264)

    def webm_download(self):
        return "/file/?filename={}".format(self.video_h264)

    def length_in_minutes(self):
        if self.length:
            length = timedelta(seconds=self.length)
            hour, minute, second = str(length).split(':')
            if int(minute) < 10:
                minute = minute[1]
            return "{}:{}".format(minute, second)

        return 0

    def next_video(self):
        try:
            videos = Video.objects.filter(
                episode__gt=self.episode).published().order_by('episode')[:1]
            return videos[0]
        except IndexError:
            return None

    def published_show_notes(self):
        md = Markdown(renderer=SyntaxHighlightRenderer())
        return md.render(self.show_notes)

    def published_transcript(self):
        md = Markdown(renderer=SyntaxHighlightRenderer())
        return md.render(self.transcript)

    def __str__(self):
        return self.title


@python_2_unicode_compatible
class Category(TimeStampedModel, TitleSlugDescriptionModel):
    image = models.CharField(max_length=255, blank=True)
    videos = models.ManyToManyField(
        Video, related_name='categories', blank=True)

    def get_absolute_url(self):
        return reverse('category', kwargs={'slug': self.slug})

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title
