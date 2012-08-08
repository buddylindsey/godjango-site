from django.conf.urls.defaults import *
from django.views.generic import TemplateView

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name="home/index.html"), name="index"),
    url(r'^about/$', TemplateView.as_view(template_name="home/about.html"), name="about"),
    url(r'^feedback/$', TemplateView.as_view(template_name="home/feedback.html"), name="feedback"),
)
