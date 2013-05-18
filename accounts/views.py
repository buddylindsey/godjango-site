from django.dispatch import receiver
from django.template import RequestContext
from django.views.generic import TemplateView
from django.shortcuts import render_to_response
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required

from episode.models import Favorite
from payments.signals import WEBHOOK_SIGNALS

def logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/')

class AccountsContextMixin(object):
    pass

class BillingView(AccountsContextMixin, TemplateView):
    template_name = 'accounts/billing.html'

class SettingsView(AccountsContextMixin, TemplateView):
    template_name = 'accounts/settings.html'

class DashboardView(AccountsContextMixin, TemplateView):
    template_name = 'accounts/dashboard.html'

@login_required()
def favorites(request):
    favorites = Favorite.objects.filter(user__id=request.user.id)
    return render_to_response('accounts/favorites.html',
        { 'favorites': favorites},
        context_instance=RequestContext(request))

@receiver(WEBHOOK_SIGNALS['customer.subscription.deleted'])
def subscription_udpated(sender, **kwargs):
    customer = named['event'].customer



