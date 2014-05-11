from django.contrib import admin

from .urls import admin_urls


def get_admin_urls(urls):
    def get_urls():
        return admin_urls + urls
    return get_urls

admin.site.get_urls = get_admin_urls(admin.site.get_urls())
