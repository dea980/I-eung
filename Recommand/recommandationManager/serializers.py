"""
레시피 추천 시스템의 데이터 직렬화를 담당하는 모듈

이 모듈은 다음과 같은 주요 기능을 위한 serializer들을 포함합니다:
- 사용자 선호도 데이터 직렬화 (UserPreferenceSerializer)
- 레시피 상호작용 데이터 직렬화 (UserRecipeInteractionSerializer)
- 추천 결과 데이터 직렬화 (RecommendationSerializer)
- 사용자 선호도 요약 정보 직렬화 (UserPreferenceSummarySerializer)
"""

from rest_framework import serializers
from django.contrib.auth.models import User
from articles.serializers import RecipeSerializer
from articles.models import Category
from .models import UserPreference, UserRecipeInteraction, RecommendationHistory

class UserPreferenceSerializer(serializers.ModelSerializer):
    """
    사용자 선호도 정보를 직렬화/역직렬화하는 serializer

    주요 기능:
    - 사용자의 식단 제한, 조리 시간, 난이도 선호도 처리
    - 알레르기 정보 정규화
    - 선호하는 카테고리 관리
    """
    favorite_categories = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=False,
        queryset=Category.objects.all(),
        required=False
    )

    class Meta:
        model = UserPreference
        fields = [
            'id', 'user', 'dietary_restriction', 'max_cooking_time',
            'preferred_difficulty', 'allergies', 'favorite_categories',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['user', 'created_at', 'updated_at']

    def validate_allergies(self, value):
        """알레르기 목록을 정규화"""
        if not value:
            return ""
        allergies = [allergy.strip() for allergy in value.split(',')]
        return ', '.join(sorted(set(allergies)))

class UserRecipeInteractionSerializer(serializers.ModelSerializer):
    """
    사용자-레시피 상호작용 정보를 직렬화/역직렬화하는 serializer

    주요 기능:
    - 레시피 조회, 저장, 요리완료, 평가 등의 상호작용 처리
    - 평가(rating) 데이터 유효성 검증
    - 상호작용 시간 기록
    """
    class Meta:
        model = UserRecipeInteraction
        fields = [
            'id', 'user', 'recipe', 'interaction_type',
            'rating', 'created_at'
        ]
        read_only_fields = ['user', 'created_at']

    def validate(self, data):
        """rating은 interaction_type이 'rate'일 때만 필요"""
        if data.get('interaction_type') == 'rate' and not data.get('rating'):
            raise serializers.ValidationError("평가 시에는 rating이 필요합니다.")
        if data.get('interaction_type') != 'rate' and data.get('rating'):
            raise serializers.ValidationError("rate 타입이 아닐 때는 rating을 포함하지 않아야 합니다.")
        return data
class RecommendationSerializer(serializers.ModelSerializer):
    """
    레시피 추천 결과를 직렬화하는 serializer

    주요 기능:
    - 추천된 레시피 상세 정보 포함
    - 추천 점수 및 추천 이유 제공
    - 사용자 상호작용 여부 표시
    """
    recipe = RecipeSerializer(read_only=True)
    
    
    class Meta:
        model = RecommendationHistory
        fields = [
            'id', 'user', 'recipe', 'score', 'reason',
            'created_at', 'interacted'
        ]
        read_only_fields = [
            'user', 'recipe', 'score', 'reason',
            'created_at', 'interacted'
        ]

class UserPreferenceSummarySerializer(serializers.ModelSerializer):
    """
    사용자 선호도의 요약 정보를 직렬화하는 serializer

    주요 기능:
    - 선호도 정보를 간단히 표시
    - 카테고리 이름을 문자열로 표현
    - 프론트엔드 표시용 최적화
    """
    favorite_categories = serializers.StringRelatedField(many=True)
    
    class Meta:
        model = UserPreference
        fields = [
            'dietary_restriction', 'max_cooking_time',
            'preferred_difficulty', 'allergies',
            'favorite_categories'
        ]