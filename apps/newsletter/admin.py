from django.contrib import admin

from .models import Event, Subscriber

admin.site.register(Event, admin.ModelAdmin)
admin.site.register(Subscriber, admin.ModelAdmin)
