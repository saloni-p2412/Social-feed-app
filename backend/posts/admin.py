from django.contrib import admin
from .models import Post, Media


class MediaInline(admin.TabularInline):
    model = Media
    extra = 0


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'text_content', 'created_at', 'published']
    list_filter = ['published', 'created_at']
    inlines = [MediaInline]


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ['id', 'post', 'media_type', 'file', 'created_at']
    list_filter = ['media_type', 'created_at']
