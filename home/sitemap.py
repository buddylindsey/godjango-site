from django.contrib.sitemaps import Sitemap

from episode.models import Video


class VideoSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5
    protocol = "https"

    def items(self):
        return Video.objects.published()
