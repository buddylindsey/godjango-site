from django.db import models
from django.conf import settings
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

class Video(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    thumbnail_image = models.CharField(max_length=200,null=True, blank=True)
    preview_image = models.CharField(max_length=200,null=True, blank=True)
    description = models.TextField()
    show_notes = models.TextField(null=True, blank=True)
    video_h264 = models.CharField(max_length=1000, null=True, blank=True)
    video_webm = models.CharField(max_length=1000, null=True, blank=True)
    length = models.PositiveIntegerField(null=True, blank=True)
    episode = models.PositiveIntegerField(null=True, blank=True)
    publish_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    favorites = models.ManyToManyField(User, through='Favorite')

    @models.permalink
    def get_absolute_url(self):
        return ('episode', (), {'pk':self.id , 'slug': self.slug})

    def _h264(self):
        if not settings.VIDEO_ROOT:
            return "/episode%s/%s" % (self.id, self.video_h264)
        else:
            return "%s/episode%s/%s" % (settings.VIDEO_ROOT, self.id, self.video_h264)
    h264 = property(_h264)

    def _webm(self):
        if not settings.VIDEO_ROOT:
            return "/episode%s/%s" % (self.id, self.video_webm)
        else:
            return "%s/episode%s/%s" % (settings.VIDEO_ROOT, self.id, self.video_webm)
    webm = property(_webm)
    
    def save(self, *args, **kwargs): 
        self.slug = slugify(self.title) 
        super(Video, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title

class Favorite(models.Model):
    user = models.ForeignKey(User)
    video = models.ForeignKey(Video)


