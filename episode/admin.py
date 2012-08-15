from django.contrib import admin
from models import Video

class VideoAdmin(admin.ModelAdmin):
    list_display = ('admin_thumbnail', 'title', 'admin_link', 'publish_date')
    list_display_links = ('admin_thumbnail', 'title')


admin.site.register(Video, VideoAdmin)
