from django.template import RequestContext
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

from cart import Cart

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

@login_required()
def cart(request):
    return render_to_response('godjango_cart/cart.html',
            { 'cart': Cart(request) },
            context_instance=RequestContext(request))

@login_required()
def checkout(request):
    return render_to_response('godjango_cart/checkout.html',
            { 'cart': Cart(request) },
            context_instance=RequestContext(request))


