from django.views.generic import ListView, DetailView

from episode.models import Video, Category


class CategoryMixin(object):
    def get_context_data(self, **kwargs):
        context = super(CategoryMixin, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class HomeView(CategoryMixin, ListView):
    model = Video
    paginate_by = 10
    queryset = Video.objects.published()
    context_object_name = "videos"
    template_name = 'home/index.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['page'] = context['paginator'].page(
            self.request.GET.get('page', '1'))
        return context


class CategoryView(CategoryMixin, DetailView):
    model = Category
    context_object_name = 'category'
    template_name = 'home/category.html'
