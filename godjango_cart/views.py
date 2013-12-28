import stripe
import json

from django.conf import settings
from django.template import RequestContext
from django.http import Http404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.views.generic import TemplateView, View
from django.utils.decorators import method_decorator

from cart import Cart
#from payments.models import Customer

from .utils import get_customer, update_email

from forms import CheckoutForm
from models import Subscription
from episode.models import Video


class AjaxResponseMixin(object):
    def render_to_json_response(self, context, **kwargs):
        data = json.dumps(context)
        kwargs['content_type'] = 'application/json'
        return HttpResponse(data, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.is_ajax():
            raise Http404

        return super(
            AjaxResponseMixin, self).dispatch(request, *args, **kwargs)


class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(
            LoginRequiredMixin, self).dispatch(request, *args, **kwargs)


class VideoMixin(object):
    def get_video(self):
        return get_object_or_404(Video, pk=self.request.POST['video_pk'])


class CartMixin(object):
    def get_cart(self):
        return Cart(self.request)


class CartView(LoginRequiredMixin, TemplateView):
    template_name = 'godjango_cart/cart.html'

    def get_context_data(self, **kwargs):
        context = super(CartView, self).get_context_data(**kwargs)
        context['cart'] = Cart(self.request)
        return context


class CartAddView(CartMixin, VideoMixin, AjaxResponseMixin, View):
    def post(self, request, *args, **kwargs):
        video = self.get_video()
        cart = self.get_cart()
        cart.add(video, video.price, 1)
        data = {'success': 'true'}
        return self.render_to_json_response(data)


class CartRemoveView(CartMixin, VideoMixin, AjaxResponseMixin, View):
    def post(self, request, *args, **kwargs):
        video = self.get_video()
        cart = self.get_cart()
        cart.remove(video)
        data = {'success': 'true'}
        return self.render_to_json_response(data)


@login_required
def checkout(request):
    if request.method == 'POST':
        cart = Cart(request)

        form = CheckoutForm(request.POST)
        if form.is_valid():
            try:
                if 'email' in request.POST:
                    update_email(request.user, request.POST.get('email'))

                customer = get_customer(request.user)

                customer.update_card(request.POST.get("stripeToken"))

                product = cart.items()[0].product

                if form.cleaned_data['coupon']:
                    customer.subscribe(
                        product.plan, coupon=form.cleaned_data['coupon'])
                else:
                    customer.subscribe(product.plan)

                cart.clear()
                return redirect("order_confirmation")

            except stripe.StripeError as e:
                try:
                    error = e.args[0]
                except IndexError:
                    error = "unknown error"

                return render_to_response('godjango_cart/checkout.html', {
                        'cart': Cart(request),
                        'publishable_key': settings.STRIPE_PUBLIC_KEY,
                        'error': error
                    },
                    context_instance=RequestContext(request))
        else:
            return render_to_response('godjango_cart/checkout.html', {
                    'cart': Cart(request),
                    'publishable_key': settings.STRIPE_PUBLIC_KEY,
                    'error': "Problem with your card please try again"
                },
                context_instance=RequestContext(request))
    else:
        return render_to_response('godjango_cart/checkout.html', {
                'cart': Cart(request),
                'publishable_key': settings.STRIPE_PUBLIC_KEY
            },
            context_instance=RequestContext(request))

@login_required()
def subscribe(request):
    cart = Cart(request)
    if cart.count() < 1:
        sub = Subscription.objects.get(plan="monthly")
        cart.add(sub, sub.price, 1)

    return redirect("checkout")
