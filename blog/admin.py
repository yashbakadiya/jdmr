from django.contrib import admin
from django.contrib.admin.options import ModelAdmin

from .models import Post, Tag, Comment, SubComment


# Register your models here.
@admin.register(Post)
class PostAdmin(ModelAdmin):
    list_display = ('id', 'title', 'author', 'views', 'timestamp', 'publish')

admin.site.register(Tag)
admin.site.register(Comment)
admin.site.register(SubComment)