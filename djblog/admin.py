from django.contrib import admin

from djblog.models import Article, Category


class ArticleAdmin(admin.ModelAdmin):
    pass


class CategoryAdmin(admin.ModelAdmin):
    filter_horizontal = ('articles',)


admin.site.register(Article, ArticleAdmin)
admin.site.register(Category, CategoryAdmin)
