from django.db.models import Q
from django.views.generic import ListView

from episode.models import Video


class SearchView(ListView):
    model = Video
    context_object_name = 'videos'
    paginate_by = 10
    template_name = 'home/browse.html'

    def get_queryset(self):
        queryset = super(SearchView, self).get_queryset()

        q = self.request.GET.get('q')
        if q:
            return queryset.filter(
                Q(description__icontains=q) | Q(title__icontains=q) |
                Q(show_notes__icontains=q)).order_by('-publish_date')

        return queryset
