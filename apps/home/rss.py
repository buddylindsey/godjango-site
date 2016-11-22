from itertools import chain
from operator import attrgetter

from django.contrib.syndication.views import Feed

from djblog.models import Article

from episode.models import Video


class LatestVideos(Feed):
        title = "GoDjango Screencasts and Tutorials"
        link = "https://godjango.com"
        description = "Tutorials covering some topic about Django."

        def items(self):
            videos = Video.objects.published().not_premium()
            articles = Article.objects.published().filter(categories__name='Tutorial')
            objects = list(chain(videos, articles))

            return sorted(objects, key=attrgetter('publish_date'), reverse=True)

        def item_title(self, item):
            return item.title

        def item_description(self, item):
            if type(item) is Article:
                return item.published_body()
            elif type(item) is Video:
                return item.description + ("<br /><a href='https://godjango.com%s'>Watch Now...</a>" % (item.get_absolute_url()))

        def item_link(self, item):
            return item.get_absolute_url()

        def item_pubdate(self, item):
            return item.publish_date


class AllContent(LatestVideos):
    def items(self):
        videos = Video.objects.published()
        articles = Article.objects.published()
        objects = list(chain(videos, articles))

        return sorted(objects, key=attrgetter('publish_date'), reverse=True)
