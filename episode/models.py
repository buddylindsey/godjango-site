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
    favorites = models.ManyToManyField(
        User, blank=True, related_name='favorites')
    is_premium = models.BooleanField(default=False)
    price = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True)
    meta_keywords = models.TextField(null=True, blank=True)

    @models.permalink
    def get_absolute_url(self):
        return ('episode', (), {'pk':self.id , 'slug': self.slug})

    def _h264(self):
        return "%sepisode-%s/%s" % (
            settings.MEDIA_URL,
            self.id, 
            self.video_h264
        )
    h264 = property(_h264)

    def _webm(self):
        return "%sepisode-%s/%s" % (
            settings.MEDIA_URL,
            self.id,
            self.video_webm
        )

    webm = property(_webm)

    def save(self, *args, **kwargs): 
        self.slug = slugify(self.title) 
        super(Video, self).save(*args, **kwargs)

    # Admin specific properties
    def admin_thumbnail(self):
        return "<img src='%s' height='41' width='66' />" % self.thumbnail_image
    admin_thumbnail.allow_tags = True

    def admin_link(self):
        return "<a href='%s'>View Video</a>" % self.get_absolute_url()
    admin_link.allow_tags = True

    def __unicode__(self):
        return self.title
