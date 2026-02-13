from django.db import models
from django.utils import timezone
import os


def media_upload_path(instance, filename):
    """Generate upload path for media files"""
    return f'posts/{instance.post.id}/{filename}'


class Post(models.Model):
    """Post model for social feed"""
    text_content = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Post {self.id} - {self.created_at}"


class Media(models.Model):
    """Media model for post images and videos"""
    MEDIA_TYPE_CHOICES = [
        ('image', 'Image'),
        ('video', 'Video'),
    ]

    post = models.ForeignKey(Post, related_name='media', on_delete=models.CASCADE)
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES)
    file = models.FileField(upload_to=media_upload_path)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.media_type} - {self.post.id}"

    @property
    def file_url(self):
        """Return the URL of the media file"""
        if self.file:
            return self.file.url
        return None
