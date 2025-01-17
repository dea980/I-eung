from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
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
    path('', RedirectView.as_view(url='/api/', permanent=False)),  # Redirect root to API root
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/auth/', include('loginManager.urls')),  # Include login manager URLs
    path('api-auth/', include('rest_framework.urls')),  # Include auth URLs for browsable API
    path('api/recommendations/', RecipeRecommendationView.as_view(), name='recipe-recommendations'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Serve media files in development
