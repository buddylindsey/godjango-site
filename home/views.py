from django.views.generic import ListView

from episode.models import Video, Category


class CategoryMixin(object):
    def get_context_data(self, **kwargs):
        context = super(CategoryMixin, self).get_context_data(**kwargs)
        context['category'] = self.get_category()
        return context


class CategoryListMixin(object):
    def get_context_data(self, **kwargs):
        context = super(CategoryListMixin, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class HomeView(CategoryListMixin, ListView):
    model = Video
    paginate_by = 10
    queryset = Video.objects.published()
    context_object_name = "videos"
    template_name = 'home/index.html'


class CategoryView(CategoryListMixin, ListView):
    model = Video
    paginate_by = 10
    context_object_name = 'videos'
    template_name = 'home/category.html'

    def get_context_data(self, **kwargs):
        context = super(CategoryView, self).get_context_data(**kwargs)
        context['category'] = self.get_category()
        return context

    def get_category(self):
        slug = self.kwargs.get('slug', None)

        if slug is not None:
            return Category.objects.get(slug=slug)
        else:
            raise AttributeError("Must use slug for urls")

    def get_queryset(self):
        return Video.objects.filter(categories=self.get_category())
