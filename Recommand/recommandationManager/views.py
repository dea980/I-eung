"""
레시피 추천 시스템의 뷰를 정의하는 모듈

이 모듈은 다음과 같은 주요 기능을 제공합니다:
- 사용자 선호도 관리 (UserPreferenceViewSet)
- 레시피 상호작용 기록 (UserRecipeInteractionViewSet)
- 개인화된 레시피 추천 (RecipeRecommendationView)
"""

from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.db.models import Count, Avg, Q
from django.shortcuts import get_object_or_404
from articles.models import Recipe, Category
from .models import (
    UserPreference, UserRecipeInteraction,
    RecipeSimilarity, RecommendationHistory
)
from .serializers import (
    UserPreferenceSerializer, UserRecipeInteractionSerializer,
    RecommendationSerializer, UserPreferenceSummarySerializer
)

class UserPreferenceViewSet(viewsets.ModelViewSet):
    """
    사용자 선호도 관리를 위한 ViewSet

    제공하는 기능:
    - 사용자별 선호도 정보 생성 및 수정
    - 선호도 정보 조회
    - 요약 정보 조회 (summary 액션)

    모든 엔드포인트는 인증된 사용자만 접근 가능합니다.
    """
    serializer_class = UserPreferenceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserPreference.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # 이미 존재하는 preference가 있으면 업데이트
        preference, created = UserPreference.objects.get_or_create(
            user=self.request.user,
            defaults=serializer.validated_data
        )
        if not created:
            for attr, value in serializer.validated_data.items():
                setattr(preference, attr, value)
            preference.save()

    @action(detail=False, methods=['get'])
    def summary(self, request):
        """사용자 선호도 요약 정보 조회"""
        preference = get_object_or_404(UserPreference, user=request.user)
        serializer = UserPreferenceSummarySerializer(preference)
        return Response(serializer.data)

class UserRecipeInteractionViewSet(viewsets.ModelViewSet):
    """
    사용자-레시피 상호작용을 관리하는 ViewSet

    제공하는 기능:
    - 레시피 조회, 저장, 요리완료, 평가 등의 상호작용 기록
    - 사용자별 상호작용 이력 조회
    - 상호작용 데이터 생성 및 수정

    모든 엔드포인트는 인증된 사용자만 접근 가능하며,
    각 사용자는 자신의 상호작용 데이터만 접근할 수 있습니다.
    """
    serializer_class = UserRecipeInteractionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserRecipeInteraction.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class RecipeRecommendationView(APIView):
    """
    개인화된 레시피 추천을 제공하는 View

    추천 알고리즘 구성:
    1. 사용자 선호도 기반 필터링
       - 식단 제한 사항 반영
       - 조리 시간 제한 적용
       - 선호하는 난이도 고려
       - 알레르기 정보 기반 필터링

    2. 추천 방식
       - 유사도 기반 추천: 사용자가 높게 평가한 레시피와 유사한 레시피 추천
       - 인기도 기반 추천: 전체 사용자들에게 높은 평가를 받은 레시피 추천
       - 카테고리 기반 추천: 사용자가 선호하는 카테고리의 레시피 추천

    3. 추천 결과
       - 각 레시피별 추천 점수 계산
       - 추천 이유 제공
       - 사용자 상호작용 추적

    모든 엔드포인트는 인증된 사용자만 접근 가능하며,
    사용자 선호도 정보가 필요합니다.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        사용자 맞춤 레시피 추천을 제공하는 메서드
        
        Returns:
            추천된 레시피 목록, 각각의 추천 점수와 추천 이유 포함
        """
        user = request.user
        try:
            preference = UserPreference.objects.get(user=user)
        except UserPreference.DoesNotExist:
            return Response(
                {"error": "사용자 선호도 설정이 필요합니다."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 기본 쿼리셋 설정
        recipes = Recipe.objects.all()

        # 사용자 선호도 기반 필터링
        if preference.dietary_restriction != 'none':
            # 여기서 dietary_restriction에 따른 필터링 로직 구현 필요
            pass

        if preference.max_cooking_time:
            recipes = recipes.filter(cooking_time__lte=preference.max_cooking_time)

        if preference.preferred_difficulty:
            recipes = recipes.filter(difficulty=preference.preferred_difficulty)

        # 알레르기 필터링
        if preference.allergies:
            allergies = [a.strip() for a in preference.allergies.split(',')]
            for allergy in allergies:
                recipes = recipes.exclude(
                    ingredients__ingredient__name__icontains=allergy
                )

        # 사용자 상호작용 기반 추천
        user_interactions = UserRecipeInteraction.objects.filter(
            user=user,
            interaction_type='rate',
            rating__gte=4
        ).values_list('recipe_id', flat=True)

        similar_recipes = RecipeSimilarity.objects.filter(
            recipe1_id__in=user_interactions
        ).order_by('-similarity_score')

        # 최종 추천 결과 생성
        recommended_recipes = []
        seen_recipes = set()

        # 1. 유사도 기반 추천
        for similarity in similar_recipes:
            if similarity.recipe2_id not in seen_recipes:
                recipe = recipes.filter(id=similarity.recipe2_id).first()
                if recipe:
                    recommended_recipes.append({
                        'recipe': recipe,
                        'score': similarity.similarity_score,
                        'reason': '비슷한 레시피를 좋아하셨네요!'
                    })
                    seen_recipes.add(recipe.id)

        # 2. 인기있는 레시피 추가
        if len(recommended_recipes) < 10:
            popular_recipes = recipes.exclude(
                id__in=seen_recipes
            ).annotate(
                avg_rating=Avg('user_interactions__rating')
            ).filter(
                avg_rating__gte=4
            ).order_by('-avg_rating')[:5]

            for recipe in popular_recipes:
                recommended_recipes.append({
                    'recipe': recipe,
                    'score': float(recipe.avg_rating),
                    'reason': '많은 사용자들이 좋아하는 레시피입니다!'
                })
                seen_recipes.add(recipe.id)

        # 3. 사용자 선호 카테고리 기반 추천
        if len(recommended_recipes) < 10:
            category_recipes = recipes.filter(
                category__in=preference.favorite_categories.all()
            ).exclude(
                id__in=seen_recipes
            ).order_by('?')[:5]

            for recipe in category_recipes:
                recommended_recipes.append({
                    'recipe': recipe,
                    'score': 0.7,  # 기본 점수
                    'reason': '선호하는 카테고리의 레시피입니다!'
                })

        # 추천 이력 저장
        for rec in recommended_recipes:
            RecommendationHistory.objects.create(
                user=user,
                recipe=rec['recipe'],
                score=rec['score'],
                reason=rec['reason']
            )

        # 응답 데이터 생성
        serializer = RecommendationSerializer([
            RecommendationHistory.objects.get(
                user=user,
                recipe=rec['recipe'],
                reason=rec['reason']
            ) for rec in recommended_recipes
        ], many=True)

        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def interaction(self, request, pk=None):
        """
        추천된 레시피에 대한 사용자 상호작용을 기록하는 메서드

        Parameters:
            request: HTTP 요청 객체 (상호작용 유형과 평점 포함)
            pk: 추천 이력 ID

        기능:
        - 추천된 레시피에 대한 사용자의 반응 기록
        - 상호작용 유형(조회, 저장, 요리완료, 평가) 저장
        - 평가인 경우 평점도 함께 저장

        Returns:
            상호작용 기록 완료 메시지
        """
        recommendation = get_object_or_404(
            RecommendationHistory,
            id=pk,
            user=request.user
        )
        recommendation.interacted = True
        recommendation.save()

        interaction_type = request.data.get('interaction_type')
        if interaction_type:
            UserRecipeInteraction.objects.create(
                user=request.user,
                recipe=recommendation.recipe,
                interaction_type=interaction_type,
                rating=request.data.get('rating')
            )

        return Response({'status': 'interaction recorded'})
