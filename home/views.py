from django.views.generic import ListView, TemplateView

from episode.mixins import CategoryListMixin
from episode.models import Video


class AboutView(TemplateView):
    template_name = 'home/about.html'


class PrivacyView(TemplateView):
    template_name = 'home/privacy.jinja'


class IndexView(CategoryListMixin, ListView):
    model = Video
    context_object_name = "videos"
    template_name = 'home/index.jinja'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['index'] = True
        context['videos'] = Video.objects.published()[:4]
        return context
