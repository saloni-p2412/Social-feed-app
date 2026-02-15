
from django.db import models


def media_upload_path(instance, filename):
    """Save media"""
    return f'posts/{instance.post.id}/{filename}'


class Post(models.Model):
    text_content = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']  # Newest first

    def __str__(self):
        return f"Post {self.id} - {self.created_at}"


class Media(models.Model):
    MEDIA_TYPE = [
        ('image', 'Image'),
        ('video', 'Video'),
    ]

    post = models.ForeignKey(Post, related_name='media', on_delete=models.CASCADE)
    media_type = models.CharField(max_length=15, choices=MEDIA_TYPE)
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
