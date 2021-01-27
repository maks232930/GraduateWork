from django.contrib import admin

from .models import (
    Portfolio,
    Category,
    Post,
    Comment,
    BlackList,
    Reader,
    Like
)

admin.site.register(Portfolio)
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(BlackList)
admin.site.register(Reader)
admin.site.register(Like)
