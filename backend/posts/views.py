from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from .models import Post, Media
from .serializers import PostSerializer, PostCreateSerializer, MediaSerializer
import os


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.filter(published=True).prefetch_related('media')
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return PostCreateSerializer
        return PostSerializer

    def list(self, request):
        """List all published posts in chronological order"""
        posts = self.queryset.all()
        serializer = self.get_serializer(posts, many=True, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        """Create a new post with optional media files"""
        # Prefer POST/FILES for multipart so form data is always available
        if request.content_type and 'multipart/form-data' in request.content_type:
            text_content = (request.POST.get('text_content') or request.data.get('text_content') or '').strip()
            published_val = request.POST.get('published', request.data.get('published', 'true'))
            files = request.FILES.getlist('media')
        else:
            text_content = (request.data.get('text_content') or '').strip()
            published_val = request.data.get('published', True)
            files = request.FILES.getlist('media')

        if not text_content and not files:
            return Response(
                {'error': 'Post must have either text content or at least one media file'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create post
        post_data = {
            'text_content': text_content or None,
            'published': published_val in (True, 'true', '1', 1)
        }
        post_serializer = PostCreateSerializer(data=post_data)
        if not post_serializer.is_valid():
            return Response(post_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        post = post_serializer.save()

        # Handle media files
        errors = []
        for file in files:
            error = self._validate_and_save_media(post, file)
            if error:
                errors.append(error)

        if errors:
            # If media validation fails, delete the post
            post.delete()
            return Response({'errors': errors}, status=status.HTTP_400_BAD_REQUEST)

        # Return created post with media
        serializer = PostSerializer(post, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def _validate_and_save_media(self, post, file):
        """Validate and save a media file"""
        # Check file size
        if file.size > settings.MAX_FILE_SIZE:
            return f"File {file.name} exceeds maximum size of {settings.MAX_FILE_SIZE / (1024*1024)}MB"

        # Check file extension
        file_ext = os.path.splitext(file.name)[1].lower()
        media_type = None

        if file_ext in settings.ALLOWED_IMAGE_EXTENSIONS:
            media_type = 'image'
        elif file_ext in settings.ALLOWED_VIDEO_EXTENSIONS:
            media_type = 'video'
        else:
            return f"File {file.name} has unsupported format. Allowed: {', '.join(settings.ALLOWED_IMAGE_EXTENSIONS + settings.ALLOWED_VIDEO_EXTENSIONS)}"

        # Save media
        Media.objects.create(post=post, media_type=media_type, file=file)
        return None
