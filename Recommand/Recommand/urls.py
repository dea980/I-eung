from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from articles.views import (
    CategoryViewSet, TagViewSet, ArticleViewSet, CommentViewSet,
    CookingToolViewSet, IngredientViewSet, RecipeViewSet, CartItemViewSet
)
from recommandationManager.views import (
    UserPreferenceViewSet, UserRecipeInteractionViewSet,
    RecipeRecommendationView
)

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'tags', TagViewSet)
router.register(r'articles', ArticleViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'cooking-tools', CookingToolViewSet)
router.register(r'ingredients', IngredientViewSet)
router.register(r'recipes', RecipeViewSet)
router.register(r'cart', CartItemViewSet, basename='cart')
router.register(r'preferences', UserPreferenceViewSet, basename='preferences')
router.register(r'recipe-interactions', UserRecipeInteractionViewSet, basename='recipe-interactions')

# API URLs
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    # Include auth URLs for browsable API
    path('api-auth/', include('rest_framework.urls')),
    # Recommendation endpoints
    path('api/recommendations/', RecipeRecommendationView.as_view(), name='recipe-recommendations'),
]
