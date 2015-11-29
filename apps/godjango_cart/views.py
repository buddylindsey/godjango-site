import stripe

from django.http import HttpResponse, Http404
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.models import User
from django.views.generic import FormView, TemplateView, View
from django.db.models import Q

from braces.views import LoginRequiredMixin

from .utils import update_email
from .forms import CheckoutForm
from .mixins import CustomerMixin

from accounts.mixins import StripeContenxtMixin
from episode.models import Video


class CheckoutView(LoginRequiredMixin, CustomerMixin, StripeContenxtMixin,
                   FormView):
    form_class = CheckoutForm
    template_name = 'godjango_cart/checkout.jinja'
    success_url = reverse_lazy('order_confirmation')
    errors = []

    def get_plan(self):
        final_plan = 'monthly'
        if 'plan' in self.request.GET:
            plan = self.request.GET.get('plan')
            if plan == 'monthly' or plan == 'yearly':
                final_plan = plan

        return final_plan

    def get_context_data(self, **kwargs):
        context = super(CheckoutView, self).get_context_data(**kwargs)
        context['plan'] = self.get_plan()
        if self.errors:
            context['errors'] = self.errors
        return context

    def form_invalid(self, form):
        self.errors.append('Problem with your card please try again')
        return super(CheckoutView, self).form_invalid(form)

    def form_valid(self, form):
        email = form.cleaned_data.get('email', None)
        if not self.request.user.email and email:
            update_email(self.request.user, email)

        if not self.request.user.email:
            self.errors.append('You do not have an email please add one')
            return super(CheckoutView, self).form_invalid(form)

        customer = self.get_customer()

        if not customer.can_charge():
            try:
                customer.update_card(
                    form.cleaned_data.get('stripeToken', None))
            except stripe.CardError:
                self.errors.append('Your card has either expired or was '
                                   'declined Please try another')
                return super(CheckoutView, self).form_invalid(form)

        plan = form.cleaned_data['plan']
        subscribe_kwargs = {}

        coupon = form.cleaned_data.get('coupon', None)
        if coupon:
            subscribe_kwargs['coupon'] = coupon

        try:
            customer.subscribe(plan, **subscribe_kwargs)
        except stripe.StripeError as e:
            try:
                error = e.args[0]
            except:
                error = 'unknown error'
            self.errors.append(error)
            return super(CheckoutView, self).form_invalid(form)

        return super(CheckoutView, self).form_valid(form)


class SubscribeView(TemplateView):
    template_name = "godjango_cart/subscribe.jinja"


class SubscriptionConfirmationView(TemplateView):
    template_name = 'godjango_cart/confirmation.jinja'


class FileView(View):
    def get_video(self, filename):
        try:
            return Video.objects.get(
                Q(video_h264=filename) | Q(video_webm=filename))
        except Video.DoesNotExist:
            raise Http404

    def download_headers(self, filename):
        response = HttpResponse()
        response['Content-Type'] = 'video/mp4'
        response["Content-Disposition"] = "attachment; filename={}".format(
            filename)
        response['X-Accel-Redirect'] = "/videos/{}".format(filename)
        return response

    def play_headers(self, filename):
        response = HttpResponse()
        response['Content-Type'] = 'video/mp4'
        response['Accept-Ranges'] = 'bytes'
        response['X-Accel-Redirect'] = "/videos/{}".format(filename)
        return response

    def video_permissions(self, request, username):
        if (request.user.is_authenticated()
                and request.user.customer.has_active_subscription()):
            return True

        if (request.user.is_authenticated()
                and not request.user.customer.has_active_subscription()):
            return False

        if not username:
            return False

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return False

        if user.customer and user.customer.has_active_subscription():
            return True

        return False

    def get(self, request, *args, **kwargs):
        filename = request.GET.get('filename', None)
        play = request.GET.get('action', None)
        username = request.GET.get('user', None)

        if not filename:
            raise Http404

        video = self.get_video(filename)

        if play and not video.is_premium:
            return self.play_headers(filename)

        premium_permission = self.video_permissions(request, username)

        if play and video.is_premium and premium_permission:
            return self.play_headers(filename)

        if not premium_permission:
            raise Http404

        return self.download_headers(filename)
