"""
Post URL routes: /api/posts/ (list, create), /api/posts/<id>/ (detail, delete)
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')

urlpatterns = [
    path('', include(router.urls)),
]
