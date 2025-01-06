from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from articles.views import (
    CategoryViewSet, TagViewSet, ArticleViewSet, CommentViewSet
)

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'tags', TagViewSet)
router.register(r'articles', ArticleViewSet)
router.register(r'comments', CommentViewSet)

# API URLs
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    # Include auth URLs for browsable API
    path('api-auth/', include('rest_framework.urls')),
]
