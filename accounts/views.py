from django.dispatch import receiver
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required

from episode.models import Favorite
from payments.signals import WEBHOOK_SIGNALS

def logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/')

@login_required()
def dashboard(request):
    return render_to_response('accounts/dashboard.html',
        { },
        context_instance=RequestContext(request))

@login_required()
def favorites(request):
    favorites = Favorite.objects.filter(user__id=request.user.id)

    return render_to_response('accounts/favorites.html',
        { 'favorites': favorites},
        context_instance=RequestContext(request))

@login_required()
def settings(request):
    return render_to_response('accounts/settings.html',
        { },
        context_instance=RequestContext(request))

@login_required()
def billing(request):
    import pdb; pdb.set_trace()
    return render_to_response('accounts/billing.html',
        { },
        context_instance=RequestContext(request))

@receiver(WEBHOOK_SIGNALS['charge.succeeded'])
def charge_succeeded(sender, **kwargs):
    print("charge_succeeded")

@login_required()
def unsubscribe(request):
    if(request.user.customer.has_active_subscription):
        request.user.customer.cancel()
        return redirect("billing")
    else:
        return redirect("billing")

