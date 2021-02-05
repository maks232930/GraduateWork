from django.contrib import admin

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
    inlines = [SocialLinkAdmin]


admin.site.register(Portfolio, PortfolioAdmin)
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(BlackList)
admin.site.register(Reader)
admin.site.register(Like)
