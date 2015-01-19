from django.http import Http404
from django.contrib.auth.models import User
from django.views.generic import DetailView, ListView, TemplateView

from newsletter.forms import NewsletterSubscribeForm

from .mixins import CategoryListMixin
from .models import Category, Video


class VideoView(DetailView):
    template_name = 'episode/video.jinja'
    model = Video
    context_object_name = 'video'

    def get_context_data(self, **kwargs):
        context = super(VideoView, self).get_context_data(**kwargs)
        context['newsletter_form'] = NewsletterSubscribeForm()
        return context


class BrowseView(CategoryListMixin, ListView):
    model = Video
    paginate_by = 10
    context_object_name = "videos"
    template_name = 'episode/browse.jinja'

    def get_context_data(self, **kwargs):
        context = super(BrowseView, self).get_context_data(**kwargs)
        context['total_videos'] = self.get_queryset().count()
        return context

    def get_queryset(self):
        qs = super(BrowseView, self).get_queryset()
        return qs.published()


class CategoryView(CategoryListMixin, ListView):
    model = Video
    paginate_by = 10
    context_object_name = 'videos'
    template_name = 'episode/category.jinja'

    def get_context_data(self, **kwargs):
        context = super(CategoryView, self).get_context_data(**kwargs)
        context['category'] = self.get_category()
        context['total_videos'] = self.get_queryset().count()
        return context

    def get_category(self):
        slug = self.kwargs.get('slug', None)

        if slug is not None:
            return Category.objects.get(slug=slug)
        else:
            raise AttributeError("Must use slug for urls")

    def get_queryset(self):
        category = self.get_category()

        qs = Video.objects.filter(categories=category).published()

        if category.series:
            return qs.order_by('episode', 'created')
        else:
            return qs.order_by('-episode', '-created')


class ProFeedView(TemplateView):
    template_name = 'episode/pro_feed.jinja'

    def verify_permission(self):
        try:
            user = User.objects.get(username=self.user)
        except User.DoesNotExist:
            raise Http404

        if user.customer and user.customer.has_active_subscription():
            return True

        return False

    def dispatch(self, request, *args, **kwargs):
        self.user = request.GET.get('user', None)
        if not self.user:
            raise Http404

        if not self.verify_permission():
            raise Http404
        return super(ProFeedView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProFeedView, self).get_context_data(**kwargs)
        context['episodes'] = Video.objects.published()
        context['username'] = self.user
        return context
