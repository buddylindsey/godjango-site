from django_jinja import library


def is_favorite(user, video):
    count = video.favorites.filter(id=user.id).count()
    if count > 0:
        return True
    return False

library.global_function(is_favorite)
