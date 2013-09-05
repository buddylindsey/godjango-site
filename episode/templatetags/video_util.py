from django import template

register = template.Library()


@register.filter
def is_favorited(video, user_id):
    count = video.favorites.filter(id=user_id).count()
    if count > 0:
        return True
    return False
