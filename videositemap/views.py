from datetime import datetime
from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template

from episode.models import Video


def video_sitemap(request):

    videos = Video.objects.filter(
        publish_date__lte=datetime.now()).order_by('-publish_date')
    ctx = {'videos': videos}

    sitemap = get_template('videositemap/xml/sitemap.xml').render(Context(ctx))

    return HttpResponse(sitemap, content_type='text/xml')
