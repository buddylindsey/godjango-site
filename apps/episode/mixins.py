from .models import Category

class CategoryListMixin(object):
    def get_context_data(self, **kwargs):
        context = super(CategoryListMixin, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

