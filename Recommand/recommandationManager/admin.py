"""
레시피 추천 시스템의 관리자 인터페이스 설정

이 모듈은 다음과 같은 모델들의 관리자 인터페이스를 제공합니다:
- 사용자 선호도 (UserPreference)
- 레시피 상호작용 (UserRecipeInteraction)
- 레시피 유사도 (RecipeSimilarity)
- 추천 이력 (RecommendationHistory)

각 모델별로 적절한 필터링, 검색, 정렬 기능을 제공합니다.
"""

from django.contrib import admin
from .models import (
    UserPreference, UserRecipeInteraction,
    RecipeSimilarity, RecommendationHistory
)

@admin.register(UserPreference)
class UserPreferenceAdmin(admin.ModelAdmin):
    list_display = ['user', 'dietary_restriction', 'preferred_difficulty', 'max_cooking_time']
    list_filter = ['dietary_restriction', 'preferred_difficulty']
    search_fields = ['user__username', 'allergies']
    filter_horizontal = ['favorite_categories']

@admin.register(UserRecipeInteraction)
class UserRecipeInteractionAdmin(admin.ModelAdmin):
    list_display = ['user', 'recipe', 'interaction_type', 'rating', 'created_at']
    list_filter = ['interaction_type', 'created_at']
    search_fields = ['user__username', 'recipe__name']
    date_hierarchy = 'created_at'

@admin.register(RecipeSimilarity)
class RecipeSimilarityAdmin(admin.ModelAdmin):
    list_display = ['recipe1', 'recipe2', 'similarity_score']
    list_filter = ['similarity_score']
    search_fields = ['recipe1__name', 'recipe2__name']

@admin.register(RecommendationHistory)
class RecommendationHistoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'recipe', 'score', 'interacted', 'created_at']
    list_filter = ['interacted', 'created_at']
    search_fields = ['user__username', 'recipe__name', 'reason']
    date_hierarchy = 'created_at'
