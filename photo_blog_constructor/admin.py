from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
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


class PostFormAdmin(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Post
        fields = '__all__'


class PostAdmin(admin.ModelAdmin):
    form = PostFormAdmin

    list_display = ('title', 'url', 'portfolio', 'category', 'client', 'budget', 'date', 'views')
    list_display_links = ('title', 'url', 'portfolio', 'category', 'client', 'budget', 'date', 'views')
    prepopulated_fields = {'url': ('title',)}
    readonly_fields = ('full_name', 'views')
    list_filter = ('category',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('reader', 'post')
    list_display_links = ('reader', 'post')


class BlackListAdmin(admin.ModelAdmin):
    list_display = ('portfolio', 'reader')
    list_display_links = ('portfolio', 'reader')


class ReaderAdmin(admin.ModelAdmin):
    list_display = ('user', 'portfolio')
    list_display_links = ('user', 'portfolio')


class LikeAdmin(admin.ModelAdmin):
    list_display = ('post', 'reader')
    list_display_links = ('post', 'reader')
    list_filter = ('post',)
    search_fields = ('post',)


admin.site.register(Portfolio, PortfolioAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(BlackList, BlackListAdmin)
admin.site.register(Reader, ReaderAdmin)
admin.site.register(Like, LikeAdmin)
