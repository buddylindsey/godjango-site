import stripe
import json

from django.conf import settings
from django.contrib import messages
from django.template import RequestContext
from django.http import Http404, HttpResponse
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.views.generic import TemplateView, View, FormView
from django.utils.decorators import method_decorator

from cart import Cart
from payments.models import Customer

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
        return get_object_or_404(Video, pk=self.request.POST.get('video_pk'))


class CartMixin(object):
    def get_cart(self):
        return Cart(self.request)

    def get_context_data(self, **kwargs):
        context = super(CartMixin, self).get_context_data(**kwargs)
        context['cart'] = self.get_cart()
        return context


class CustomerMixin(object):
    def get_customer(self):
        try:
            return self.request.user.customer
        except:
            return Customer.create(self.request.user)


class CartView(LoginRequiredMixin, CartMixin, TemplateView):
    template_name = 'godjango_cart/cart.html'


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


class CheckoutView(CustomerMixin, CartMixin, FormView):
    form_class = CheckoutForm
    template_name = 'godjango_cart/checkout.html'
    success_url = reverse_lazy('order_confirmation')
    errors = []

    def get_context_data(self, **kwargs):
        context = super(CheckoutView, self).get_context_data(**kwargs)
        context['publishable_key'] = settings.STRIPE_PUBLIC_KEY
        if self.errors:
            context['errors'] = self.errors
        return context

    def form_invalid(self, form):
        self.errors.append('Problem with your card please try again')
        return super(CheckoutView, self).form_invalid(form)

    def form_valid(self, form):
        form_kwargs = self.get_form_kwargs()

        cart = self.get_cart()

        if 'email' in form_kwargs.get('data'):
            update_email(self.request.user, form_kwargs.get('data')['email'])

        customer = self.get_customer()

        if not customer.can_charge():
            customer.update_card(form.cleaned_data.get('stripeToken', None))

        product = cart.items()[0].product

        subscribe_kwargs = {}
        if form.cleaned_data.get('coupon') != '':
            subscribe_kwargs['coupon'] = form.cleaned_data.get('coupon')

        try:
            customer.subscribe(product.plan, **subscribe_kwargs)
        except stripe.StripeError as e:
            try:
                error = e.args[0]
            except:
                error = 'unknown error'
            self.errors.append(error)
            return super(CheckoutView, self).form_invalid(form)

        cart.clear()

        return super(CheckoutView, self).form_valid(form)


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
