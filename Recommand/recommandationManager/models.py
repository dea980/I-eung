"""
사용자 맞춤 레시피 추천 시스템을 위한 모델 정의

이 모듈은 다음과 같은 주요 기능을 위한 모델들을 포함합니다:
- 사용자 선호도 관리 (UserPreference)
- 레시피 상호작용 추적 (UserRecipeInteraction)
- 레시피 간 유사도 계산 (RecipeSimilarity)
- 추천 이력 관리 (RecommendationHistory)
"""

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from articles.models import Recipe

class UserPreference(models.Model):
    """
    사용자의 요리 및 식사 선호도를 저장하는 모델

    주요 필드:
    - dietary_restriction: 식단 제한 사항 (채식, 비건 등)
    - max_cooking_time: 선호하는 최대 조리 시간
    - preferred_difficulty: 선호하는 레시피 난이도
    - allergies: 알레르기 정보
    - favorite_categories: 선호하는 요리 카테고리
    """
    DIETARY_CHOICES = [
        ('none', '제한 없음'),
        ('vegetarian', '채식주의'),
        ('vegan', '비건'),
        ('pescatarian', '페스코'),
        ('gluten_free', '글루텐프리'),
        ('dairy_free', '유제품 제외'),
    ]

    SKILL_LEVEL_CHOICES = [
        ('beginner', '초보자'),
        ('intermediate', '중급자'),
        ('advanced', '고급자'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='preferences')
    dietary_restriction = models.CharField(max_length=20, choices=DIETARY_CHOICES, default='none')
    max_cooking_time = models.PositiveIntegerField(help_text="선호하는 최대 조리 시간(분)", null=True, blank=True)
    preferred_difficulty = models.CharField(max_length=20, choices=SKILL_LEVEL_CHOICES, default='beginner')
    allergies = models.TextField(blank=True, help_text="콤마로 구분된 알레르기 목록")
    favorite_categories = models.ManyToManyField('articles.Category', related_name='preferred_by_users', blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s preferences"

class UserRecipeInteraction(models.Model):
    """
    사용자와 레시피 간의 상호작용을 기록하는 모델

    주요 필드:
    - user: 상호작용한 사용자
    - recipe: 상호작용한 레시피
    - interaction_type: 상호작용 유형 (조회, 저장, 요리완료, 평가)
    - rating: 레시피 평가 점수 (1-5점)
    - created_at: 상호작용 발생 시간
    """
    INTERACTION_TYPES = [
        ('view', '조회'),
        ('save', '저장'),
        ('cook', '요리완료'),
        ('rate', '평가'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipe_interactions')
    recipe = models.ForeignKey('articles.Recipe', on_delete=models.CASCADE, related_name='user_interactions')
    interaction_type = models.CharField(max_length=10, choices=INTERACTION_TYPES)
    rating = models.PositiveSmallIntegerField(null=True, blank=True, validators=[
        MinValueValidator(1),
        MaxValueValidator(5)
    ])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'recipe', 'interaction_type']
        indexes = [
            models.Index(fields=['user', 'interaction_type']),
            models.Index(fields=['recipe', 'interaction_type']),
        ]

    def __str__(self):
        return f"{self.user.username} {self.interaction_type} {self.recipe.name}"

class RecipeSimilarity(models.Model):
    """
    레시피 간의 유사도를 저장하는 모델

    주요 필드:
    - recipe1: 비교 대상 레시피 1
    - recipe2: 비교 대상 레시피 2
    - similarity_score: 두 레시피 간의 유사도 점수 (0-1 사이의 값)
    """
    recipe1 = models.ForeignKey('articles.Recipe', on_delete=models.CASCADE, related_name='similar_to')
    recipe2 = models.ForeignKey('articles.Recipe', on_delete=models.CASCADE, related_name='similar_from')
    similarity_score = models.FloatField(help_text="레시피 간 유사도 점수 (0-1)")
    
    class Meta:
        unique_together = ['recipe1', 'recipe2']
        indexes = [
            models.Index(fields=['recipe1', 'similarity_score']),
            models.Index(fields=['recipe2', 'similarity_score']),
        ]

    def __str__(self):
        return f"Similarity between {self.recipe1.name} and {self.recipe2.name}: {self.similarity_score}"

class RecommendationHistory(models.Model):
    """
    사용자별 레시피 추천 이력을 저장하는 모델

    주요 필드:
    - user: 추천을 받은 사용자
    - recipe: 추천된 레시피
    - score: 추천 알고리즘이 계산한 추천 점수
    - reason: 해당 레시피가 추천된 이유
    - interacted: 사용자가 추천에 반응했는지 여부
    - created_at: 추천이 생성된 시간
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recommendation_history')
    recipe = models.ForeignKey('articles.Recipe', on_delete=models.CASCADE, related_name='recommendation_history')
    score = models.FloatField(help_text="추천 점수")
    reason = models.CharField(max_length=200, help_text="추천 이유")
    created_at = models.DateTimeField(auto_now_add=True)
    interacted = models.BooleanField(default=False, help_text="사용자가 추천에 반응했는지 여부")

    class Meta:
        indexes = [
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['user', 'interacted']),
        ]

    def __str__(self):
        return f"Recommendation of {self.recipe.name} for {self.user.username}"
