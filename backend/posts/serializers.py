
from rest_framework import serializers
from .models import Post, Media


class MediaSerializer(serializers.ModelSerializer):

    file_url = serializers.SerializerMethodField()

    class Meta:
        model = Media
        fields = ['id', 'media_type', 'file_url', 'created_at']

    def get_file_url(self, obj):
        try:
            url = obj.file.url if obj.file else None
        except (ValueError, OSError):
            url = None
        if not url:
            return None
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(url)
        return url


class PostSerializer(serializers.ModelSerializer):
    media = MediaSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'text_content', 'created_at', 'published', 'media']
        read_only_fields = ['id', 'created_at']


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['text_content', 'published']
