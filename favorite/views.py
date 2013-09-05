import json
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods

from episode.models import Video


@require_http_methods(["POST"])
def toggle_favorite(request):
    video = Video.objects.get(pk=request.POST['video_pk'])

    if request.POST['is_favorite'] == 'true':
        request.user.favorites.remove(video)
        return HttpResponse(
            json.dumps({"success": True}), content_type="application/json")
    else:
        request.user.favorites.add(video)
        return HttpResponse(
            json.dumps({"success": True}), content_type="application/json")

    return HttpResponse(
        json.dumps({"success": False}), content_type="application/json")
