from django.conf.urls import *
from django.views.generic import TemplateView, ListView

from episode.models import Video

urlpatterns = patterns('',
        url(r'^$', ListView.as_view(
            model=Video, 
            paginate_by='10',
            queryset=Video.objects.all(),
            context_object_name="videos",
            template_name='home/index.html'), name="index"),
        url(r'^$', TemplateView.as_view(template_name="home/index.html"), name="index"),
        url(r'^about/$', TemplateView.as_view(template_name="home/about.html"), name="about"),
        url(r'^feedback/$', TemplateView.as_view(template_name="home/feedback.html"), name="feedback"),
        )
