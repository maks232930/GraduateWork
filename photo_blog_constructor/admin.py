from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import (
    Category,
    Post,
    Photo,
    Comment,
    Reader,
    Like,
    SocialLink,
    Portfolio,
    Contact
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
        return mark_safe(f'<img src="{obj.logo.url}" height="50px" width="50px">')


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

    list_display = ('title', 'url', 'portfolio', 'category', 'date', 'views')
    list_display_links = ('title', 'url', 'portfolio', 'category', 'date', 'views')
    prepopulated_fields = {'url': ('title',)}
    readonly_fields = ('views',)
    list_filter = ('category',)


class PhotoAdmin(admin.ModelAdmin):
    list_display = ('post',)
    list_filter = ('post',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('reader', 'post')
    list_display_links = ('reader', 'post')


class ReaderAdmin(admin.ModelAdmin):
    list_display = ('user', 'portfolio')
    list_display_links = ('user', 'portfolio')


class LikeAdmin(admin.ModelAdmin):
    list_display = ('post', 'reader')
    list_display_links = ('post', 'reader')
    list_filter = ('post',)
    search_fields = ('post',)


class ContactAdmin(admin.ModelAdmin):
    list_display = ('portfolio', 'name', 'email', 'message', 'is_read')


admin.site.register(Portfolio, PortfolioAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Reader, ReaderAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(Contact, ContactAdmin)
