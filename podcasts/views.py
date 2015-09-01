from django.views.generic import ListView

from djblog.models import Article


class PodcastListView(ListView):
    template_name = 'podcasts/index.jinja'
    model = Article
    context_object_name = 'podcasts'

    def get_queryset(self):
        qs = super(PodcastListView, self).get_queryset()
        return qs.published().filter(
            categories__slug='podcast').order_by('-publish_date')
