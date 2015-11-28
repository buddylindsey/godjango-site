from django.contrib import admin
from models import Video, Category, Transcript
from django.template.response import TemplateResponse


class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'publish_date', 'is_premium')
    list_display_links = ('title',)
    exclude = ('favorites',)
    list_filter = ('is_premium',)
    readonly_fields = ('slug',)
    actions = ('generate_social_urls',)

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

    def generate_social_urls(self, request, queryset):
        context = {
            'queryset': queryset
        }
        return TemplateResponse(
            request, ['admin/social_urls.html'],
            context, current_app=self.admin_site.name)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'total_videos',)
    filter_horizontal = ('videos',)

    def total_videos(self, obj):
        return obj.videos.count()
    total_videos.short_description = 'Total Videos in Category'


class TranscriptAdmin(admin.ModelAdmin):
    raw_id_fields = ('video',)
    list_display = ('video', 'label')
    list_filter = ('srclang',)

    fieldsets = (
        (None, {'fields': ('video',)}),
        ('File', {'fields': ('file',)}),
        ('Language', {'fields': ('srclang', 'label')})
    )


admin.site.register(Video, VideoAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Transcript, TranscriptAdmin)
