from django.conf import settings


class StripeContenxtMixin(object):
    def get_context_data(self, **kwargs):
        context = super(StripeContenxtMixin, self).get_context_data(**kwargs)
        context['publishable_key'] = settings.STRIPE_PUBLIC_KEY
        return context


class NextUrlMixin(object):
    def get_success_url(self):
        if 'next' in self.request.GET:
            return self.request.GET.get('next')

        return super(NextUrlMixin, self).get_success_url()

class LastAccessMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            request.user.profile.update_last_access()
        return super(LastAccessMixin, self).dispatch(request, *args, **kwargs)
