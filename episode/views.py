from django.views.generic import DetailView

from accounts.forms import NewsletterSubscribeForm

from .models import Video

class VideoView(DetailView):
    template_name = 'episode/video.html'
    model = Video
    context_object_name = 'video'

    def get_context_data(self, **kwargs):
        context = super(VideoView, self).get_context_data(**kwargs)
        context['newsletter_form'] = NewsletterSubscribeForm()
        return context
