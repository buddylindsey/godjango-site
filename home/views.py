from django.views.generic import ListView, TemplateView

from episode.mixins import CategoryListMixin
from episode.models import Video


class AboutView(TemplateView):
    template_name = 'home/about.jinja'


class PrivacyView(TemplateView):
    template_name = 'home/privacy.jinja'


class IndexView(CategoryListMixin, ListView):
    model = Video
    context_object_name = "videos"
    template_name = 'home/index.jinja'
    paginate_by = 8

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['index'] = True
        return context

    def get_queryset(self):
        qs = super(IndexView, self).get_queryset()
        return qs.published()
