from django.contrib import admin
from models import Video, Category


class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'publish_date', 'is_premium')
    list_display_links = ('title',)
    exclude = ('favorites',)
    list_filter = ('is_premium',)
    readonly_fields = ('slug',)

    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'publish_date')
        }),
        ('Images', {
            'fields': ('preview_image', 'thumbnail_image')
        }),
        ('Video Location', {
            'fields': ('video_h264', 'video_webm', 'youtube_id')
        }),
        ('Meta', {
            'fields': ('widescreen', 'is_premium', 'revised', 'price',
                       'length', 'episode')
        }),
        ('Data', {
            'fields': ('description', 'show_notes', 'transcript')
        }),
    )


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'total_videos',)
    filter_horizontal = ('videos',)

    def total_videos(self, obj):
        return obj.videos.count()
    total_videos.short_description = 'Total Videos in Category'


admin.site.register(Video, VideoAdmin)
admin.site.register(Category, CategoryAdmin)
