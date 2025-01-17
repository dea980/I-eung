from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, OAuthProfile

class UserSerializer(serializers.ModelSerializer):
    """
    사용자 정보 시리얼라이저
    """
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    """
    사용자 프로필 시리얼라이저
    """
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = ('id', 'user', 'nickname', 'bio', 'birth_date', 'profile_image', 
                 'created_at', 'updated_at')

class OAuthProfileSerializer(serializers.ModelSerializer):
    """
    OAuth 프로필 시리얼라이저
    """
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = OAuthProfile
        fields = ('id', 'user', 'provider', 'oauth_user_id', 'expires_at', 
                 'created_at', 'updated_at')
        read_only_fields = ('access_token', 'refresh_token')

class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    사용자 등록을 위한 시리얼라이저
    """
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'confirm_password', 
                 'first_name', 'last_name')

    def validate(self, data):
        if data['password'] != data.pop('confirm_password'):
            raise serializers.ValidationError("비밀번호가 일치하지 않습니다.")
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        UserProfile.objects.create(user=user)
        return user

class PasswordChangeSerializer(serializers.Serializer):
    """
    비밀번호 변경 시리얼라이저
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_new_password = serializers.CharField(required=True)

    def validate(self, data):
        if data['new_password'] != data['confirm_new_password']:
            raise serializers.ValidationError("새 비밀번호가 일치하지 않습니다.")
        return data

class LoginSerializer(serializers.Serializer):
    """
    로그인 시리얼라이저
    """
    username = serializers.CharField()
    password = serializers.CharField()

class OAuthLoginSerializer(serializers.Serializer):
    """
    OAuth 로그인 시리얼라이저
    """
    provider = serializers.CharField()
    access_token = serializers.CharField()
    
    def validate_provider(self, value):
        if value not in ['google', 'kakao']:
            raise serializers.ValidationError("지원하지 않는 OAuth 제공자입니다.")