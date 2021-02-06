from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import (
    Portfolio,
    Category,
    Post,
    Comment,
    BlackList,
    Reader,
    Like,
    SocialLink
)


class SocialLinkAdmin(admin.StackedInline):
    model = SocialLink
    extra = 1
    show_change_link = True


class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'slug', 'get_logo')
    list_display_links = ('user', 'name', 'slug')
    list_filter = ('name',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    inlines = [SocialLinkAdmin]

    def get_logo(self, obj):
        return mark_safe(f'<img src="{obj.logo.url}">')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'portfolio')
    list_display_links = ('name', 'slug', 'portfolio')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'portfolio', 'category', 'client', 'budget', 'date', 'views')
    list_display_links = ('title', 'slug', 'portfolio', 'category', 'client', 'budget', 'date', 'views')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('full_name', 'views')
    list_filter = ('category',)


admin.site.register(Portfolio, PortfolioAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(BlackList)
admin.site.register(Reader)
admin.site.register(Like)
