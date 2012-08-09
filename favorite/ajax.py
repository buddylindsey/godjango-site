from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from episode.models import Video, Favorite

def add_favorite(request):
    if(request.is_ajax() and request.POST):
        user = get_object_or_404(User, pk=request.POST['user_pk'])
        video = get_object_or_404(Video, pk=request.POST['video_pk'])

        fav = Favorite()
        fav.video = video
        fav.user = user
        fav.save()

        if fav.id:
            return HttpResponse("{'success':true}")
        else:
            return HttpResponse("{'success':false}")
    else:
        raise Http404
