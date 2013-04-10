from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required

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
    return render_to_response('accounts/favorites.html',
        { },
        context_instance=RequestContext(request))

@login_required()
def settings(request):
    return render_to_response('accounts/settings.html',
        { },
        context_instance=RequestContext(request))

@login_required()
def billing(request):
    return render_to_response('accounts/billing.html',
        { },
        context_instance=RequestContext(request))

