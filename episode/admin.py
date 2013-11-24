from django.contrib import admin
from models import Video, Category


class VideoAdmin(admin.ModelAdmin):
    list_display = ('admin_thumbnail', 'title', 'admin_link', 'publish_date')
    list_display_links = ('admin_thumbnail', 'title')
    exclude = ('favorites',)


class CategoryAdmin(admin.ModelAdmin):
    pass


admin.site.register(Video, VideoAdmin)
admin.site.register(Category, CategoryAdmin)
