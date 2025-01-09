from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db.models import Count, Avg, Q, Sum
from django.contrib.auth.models import User
from .models import (
    Category, Tag, Article, Comment, Rating, Like, Dislike,
    CookingTool, Ingredient, Recipe, RecipeStep, RecipeIngredient, CartItem
)
from .serializers import (
    CategorySerializer, TagSerializer, ArticleSerializer,
    CommentSerializer, RatingSerializer, LikeSerializer, DislikeSerializer,
    CookingToolSerializer, IngredientSerializer, RecipeSerializer,
    RecipeStepSerializer, RecipeIngredientSerializer, CartItemSerializer
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
            Like.objects.filter(article=article, user=request.user).delete()
            return Response({'status': 'disliked'})
        return Response({'status': 'already disliked'})

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['content', 'author__username']
    ordering_fields = ['created_at', 'updated_at']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

# New viewsets for cooking and shopping features

class CookingToolViewSet(viewsets.ModelViewSet):
    queryset = CookingTool.objects.all()
    serializer_class = CookingToolSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']

class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'name']

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def add_to_cart(self, request, pk=None):
        ingredient = self.get_object()
        quantity = int(request.data.get('quantity', 1))

        if quantity > ingredient.stock:
            return Response(
                {'error': f'재고가 부족합니다. 현재 재고: {ingredient.stock}'},
                status=status.HTTP_400_BAD_REQUEST
            )

        cart_item, created = CartItem.objects.get_or_create(
            user=request.user,
            ingredient=ingredient,
            defaults={'quantity': quantity}
        )

        if not created:
            cart_item.quantity += quantity
            if cart_item.quantity > ingredient.stock:
                return Response(
                    {'error': f'재고가 부족합니다. 현재 재고: {ingredient.stock}'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            cart_item.save()

        return Response({'status': 'added to cart', 'quantity': cart_item.quantity})

class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description', 'author__username']
    ordering_fields = ['created_at', 'cooking_time', 'difficulty']

    def get_queryset(self):
        queryset = Recipe.objects.all()
        difficulty = self.request.query_params.get('difficulty', None)
        max_time = self.request.query_params.get('max_time', None)
        tool = self.request.query_params.get('tool', None)

        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)
        if max_time:
            queryset = queryset.filter(cooking_time__lte=int(max_time))
        if tool:
            queryset = queryset.filter(tools__name=tool)

        return queryset.distinct()

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def add_ingredients_to_cart(self, request, pk=None):
        recipe = self.get_object()
        serving_size = int(request.data.get('serving_size', 1))
        
        if serving_size < 1:
            return Response(
                {'error': '올바른 인분 수를 입력해주세요.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        recipe_ingredients = recipe.ingredients.all()
        added_items = []
        errors = []

        for recipe_ingredient in recipe_ingredients:
            required_quantity = recipe_ingredient.quantity * serving_size
            ingredient = recipe_ingredient.ingredient

            if required_quantity > ingredient.stock:
                errors.append(f'{ingredient.name}: 재고 부족 (필요: {required_quantity}{recipe_ingredient.unit}, 재고: {ingredient.stock}{ingredient.unit})')
                continue

            cart_item, created = CartItem.objects.get_or_create(
                user=request.user,
                ingredient=ingredient,
                defaults={'quantity': required_quantity}
            )

            if not created:
                cart_item.quantity += required_quantity
                if cart_item.quantity > ingredient.stock:
                    errors.append(f'{ingredient.name}: 재고 부족 (필요: {cart_item.quantity}{recipe_ingredient.unit}, 재고: {ingredient.stock}{ingredient.unit})')
                    continue
                cart_item.save()

            added_items.append(f'{ingredient.name}: {required_quantity}{recipe_ingredient.unit}')

        response_data = {
            'added_items': added_items,
            'errors': errors
        }

        if errors:
            response_data['status'] = 'partially_added'
        else:
            response_data['status'] = 'all_added'

        return Response(response_data)

class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at']

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def summary(self, request):
        cart_items = self.get_queryset()
        total_price = sum(item.total_price for item in cart_items)
        
        return Response({
            'total_items': cart_items.count(),
            'total_price': total_price,
            'items': CartItemSerializer(cart_items, many=True).data
        })

    @action(detail=False, methods=['post'])
    def clear(self, request):
        self.get_queryset().delete()
        return Response({'status': 'cart cleared'})