from django.http import Http404, HttpResponsePermanentRedirect
from django.contrib.auth.models import User
from django.views.generic import DetailView, ListView, TemplateView

from newsletter.forms import NewsletterSubscribeForm

from accounts.mixins import LastAccessMixin

from .mixins import CategoryListMixin
from .models import Category, Video


class VideoView(LastAccessMixin, DetailView):
    template_name = 'episode/video.jinja'
    model = Video
    context_object_name = 'video'
    pk_url_kwarg = 'episode'
    redirect = False

    def get_context_data(self, **kwargs):
        context = super(VideoView, self).get_context_data(**kwargs)
        context['newsletter_form'] = NewsletterSubscribeForm()
        context['related_videos'] = self.get_related_videos()
        return context

    def get_related_videos(self):
        videos = self.object.categories.all().order_by('-series')
        if not videos.exists():
            return {}

        return videos[0].videos.all()[:5]

    def get_object(self, queryset=None):
        episode = self.kwargs.get('episode')
        slug = self.kwargs.get('slug')
        try:
            return Video.objects.get(episode=episode, slug=slug)
        except Video.DoesNotExist:
            self.redirect = True
            return self.video_redirect(episode, slug)

    def video_redirect(self, episode, slug):
        video = Video.objects.filter(episode=episode)
        if 'revised' in slug:
            return video.latest()
        else:
            return video.exclude(slug__contains='revised').get()

    def get(self, request, *args, **kwargs):
        response = super(VideoView, self).get(request, *args, **kwargs)
        if self.redirect:
            return HttpResponsePermanentRedirect(
                self.object.get_absolute_url())
        return response


class BrowseView(LastAccessMixin, CategoryListMixin, ListView):
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


class CategoryView(LastAccessMixin, CategoryListMixin, ListView):
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

        return qs.order_by('-episode', '-created_at')


class SeriesView(CategoryView):
    def get_queryset(self):
        category = self.get_category()
        qs = Video.objects.filter(categories=category).published()
        return qs.order_by('episode', 'created_at')



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

    def get(self, request, *args, **kwargs):
        response = super(ProFeedView, self).get(request, args, kwargs)
        response['Content-Type'] = 'application/rss+xml'
        return response
