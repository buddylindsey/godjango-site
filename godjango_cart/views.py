import stripe

from django.conf import settings
from django.template import RequestContext
from django.http import Http404, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render_to_response, redirect

from cart import Cart
from payments.models import Customer

from forms import CheckoutForm
from models import Subscription
from episode.models import Video

def add(request):
    if(request.is_ajax() and request.POST):
        video = get_object_or_404(Video, pk=request.POST['video_pk'])
        cart = Cart(request)
        cart.add(video, video.price, 1)
        return HttpResponse("{'success':true}", mimetype="application/json")
    else:
        raise Http404

def remove(request):
    if(request.is_ajax() and request.POST):
        video = get_object_or_404(Video, pk=request.POST['video_pk'])
        cart = Cart(request)
        cart.remove(video)
        return HttpResponse("{'success':true}", mimetype="application/json")
    else:
        raise Http404

@login_required
def cart(request):
    return render_to_response('godjango_cart/cart.html',
            { 'cart': Cart(request) },
            context_instance=RequestContext(request))


@login_required
def checkout(request):
    if request.POST:
        cart = Cart(request)

        form = CheckoutForm(request.POST)
        if form.is_valid():
            try:
                try:
                    customer = request.user.customer
                except ObjectDoesNotExist:
                    customer = Customer.create(request.user)
                customer.update_card(request.POST.get("stripeToken"))

                if(cart.count() == 1):
                    item = cart.items()[0]

                    if(type(item.product) is Subscription):
                        customer.subscribe(item.plan)
                    else:
                        customer.charge(cart.summary(), 'usd', request.user.username)
                else:
                    customer.charge(cart.summary(), 'usd', request.user.username)

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
        return render_to_response('godjango_cart/checkout.html',
            { 'cart': Cart(request), 'publishable_key': settings.STRIPE_PUBLIC_KEY },
            context_instance=RequestContext(request))

@login_required()
def subscribe(request):
    cart = Cart(request)
    sub = Subscription.objects.get(plan="monthly")
    cart.add(sub, sub.price, 1)

    return redirect("checkout")
