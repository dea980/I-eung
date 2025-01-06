from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db.models import Count, Avg, Q
from django.contrib.auth.models import User
from .models import Category, Tag, Article, Comment, Rating, Like, Dislike
from .serializers import (
    CategorySerializer, TagSerializer, ArticleSerializer,
    CommentSerializer, RatingSerializer, LikeSerializer, DislikeSerializer
)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content', 'author__username', 'category__name', 'tags__name']
    ordering_fields = ['created_at', 'updated_at', 'views_count', 'likes_count']

    def get_queryset(self):
        queryset = Article.objects.all()
        category = self.request.query_params.get('category', None)
        tag = self.request.query_params.get('tag', None)
        author = self.request.query_params.get('author', None)

        if category:
            queryset = queryset.filter(category__name=category)
        if tag:
            queryset = queryset.filter(tags__name=tag)
        if author:
            queryset = queryset.filter(author__username=author)

        return queryset.distinct()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views_count += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        article = self.get_object()
        like, created = Like.objects.get_or_create(
            article=article,
            user=request.user
        )
        if created:
            article.likes_count += 1
            article.save()
            # Remove dislike if exists
            Dislike.objects.filter(article=article, user=request.user).delete()
            return Response({'status': 'liked'})
        return Response({'status': 'already liked'})

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def dislike(self, request, pk=None):
        article = self.get_object()
        dislike, created = Dislike.objects.get_or_create(
            article=article,
            user=request.user
        )
        if created:
            article.dislikes_count += 1
            article.save()
            # Remove like if exists
            Like.objects.filter(article=article, user=request.user).delete()
            return Response({'status': 'disliked'})
        return Response({'status': 'already disliked'})

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def rate(self, request, pk=None):
        article = self.get_object()
        value = request.data.get('value')
        
        if not value or not isinstance(value, int) or value < 1 or value > 5:
            return Response(
                {'error': 'Invalid rating value'},
                status=status.HTTP_400_BAD_REQUEST
            )

        rating, created = Rating.objects.update_or_create(
            article=article,
            user=request.user,
            defaults={'value': value}
        )
        
        return Response({'status': 'rated', 'value': value})

    @action(detail=False, methods=['get'])
    def recommended(self, request):
        if not request.user.is_authenticated:
            return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)

        # Get user's liked articles
        liked_articles = Article.objects.filter(likes__user=request.user)
        
        # Get tags from liked articles
        liked_tags = Tag.objects.filter(articles__in=liked_articles).distinct()
        
        # Get categories from liked articles
        liked_categories = Category.objects.filter(articles__in=liked_articles).distinct()
        
        # Find similar articles based on tags and categories
        recommended = Article.objects.exclude(
            id__in=liked_articles.values_list('id', flat=True)
        ).filter(
            Q(tags__in=liked_tags) | Q(category__in=liked_categories)
        ).annotate(
            avg_rating=Avg('ratings__value'),
            like_count=Count('likes'),
            relevance_score=Count('tags', filter=Q(tags__in=liked_tags)) + 
                          Count('category', filter=Q(category__in=liked_categories))
        ).order_by('-relevance_score', '-avg_rating', '-like_count')[:10]
        
        serializer = self.get_serializer(recommended, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def top_rated(self, request):
        top_articles = Article.objects.annotate(
            avg_rating=Avg('ratings__value')
        ).filter(
            avg_rating__isnull=False
        ).order_by('-avg_rating', '-created_at')[:10]
        
        serializer = self.get_serializer(top_articles, many=True)
        return Response(serializer.data)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['content', 'author__username']
    ordering_fields = ['created_at', 'updated_at']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        queryset = Comment.objects.all()
        article_id = self.request.query_params.get('article', None)
        if article_id:
            queryset = queryset.filter(article_id=article_id)
        return queryset