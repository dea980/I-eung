from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import UserProfile, OAuthProfile
from .serializers import (
    UserSerializer, UserProfileSerializer, OAuthProfileSerializer,
    UserRegistrationSerializer, PasswordChangeSerializer, LoginSerializer,
    OAuthLoginSerializer
)
from django.conf import settings
from datetime import datetime, timedelta
import requests
import json

class UserViewSet(viewsets.ModelViewSet):
    """
    사용자 관리를 위한 ViewSet
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'login', 'oauth_login']:
            return [AllowAny()]
        return super().get_permissions()

    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': '회원가입이 완료되었습니다.',
                'user': UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password']
            )
            if user:
                login(request, user)
                return Response({
                    'message': '로그인 성공',
                    'user': UserSerializer(user).data
                })
            return Response({
                'message': '아이디 또는 비밀번호가 잘못되었습니다.'
            }, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def logout(self, request):
        logout(request)
        return Response({'message': '로그아웃 되었습니다.'})

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def change_password(self, request):
        serializer = PasswordChangeSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if user.check_password(serializer.validated_data['old_password']):
                user.set_password(serializer.validated_data['new_password'])
                user.save()
                return Response({'message': '비밀번호가 변경되었습니다.'})
            return Response({
                'message': '현재 비밀번호가 잘못되었습니다.'
            }, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileViewSet(viewsets.ModelViewSet):
    """
    사용자 프로필 관리를 위한 ViewSet
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)

class OAuthLoginView(APIView):
    """
    OAuth 로그인을 처리하는 View
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = OAuthLoginSerializer(data=request.data)
        if serializer.is_valid():
            provider = serializer.validated_data['provider']
            access_token = serializer.validated_data['access_token']

            if provider == 'google':
                return self.handle_google_login(access_token)
            elif provider == 'kakao':
                return self.handle_kakao_login(access_token)
            
            return Response({
                'message': '지원하지 않는 OAuth 제공자입니다.'
            }, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def handle_google_login(self, access_token):
        try:
            # Google 사용자 정보 가져오기
            response = requests.get(
                'https://www.googleapis.com/oauth2/v3/userinfo',
                headers={'Authorization': f'Bearer {access_token}'}
            )
            if response.status_code != 200:
                return Response({
                    'message': 'Google OAuth 토큰이 유효하지 않습니다.'
                }, status=status.HTTP_401_UNAUTHORIZED)

            user_data = response.json()
            oauth_user_id = user_data['sub']

            # 기존 OAuth 프로필 확인
            oauth_profile = OAuthProfile.objects.filter(
                provider='google',
                oauth_user_id=oauth_user_id
            ).first()

            if oauth_profile:
                # 기존 사용자 로그인
                login(self.request, oauth_profile.user)
                return Response({
                    'message': '로그인 성공',
                    'user': UserSerializer(oauth_profile.user).data
                })

            # 새 사용자 생성
            user = User.objects.create_user(
                username=f"google_{oauth_user_id}",
                email=user_data.get('email', ''),
                first_name=user_data.get('given_name', ''),
                last_name=user_data.get('family_name', '')
            )

            # 프로필 생성
            UserProfile.objects.create(user=user)

            # OAuth 프로필 생성
            OAuthProfile.objects.create(
                user=user,
                provider='google',
                oauth_user_id=oauth_user_id,
                access_token=access_token,
                expires_at=datetime.now() + timedelta(hours=1)
            )

            login(self.request, user)
            return Response({
                'message': '회원가입 및 로그인 성공',
                'user': UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({
                'message': f'Google OAuth 처리 중 오류가 발생했습니다: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def handle_kakao_login(self, access_token):
        try:
            # Kakao 사용자 정보 가져오기
            response = requests.get(
                'https://kapi.kakao.com/v2/user/me',
                headers={'Authorization': f'Bearer {access_token}'}
            )
            if response.status_code != 200:
                return Response({
                    'message': 'Kakao OAuth 토큰이 유효하지 않습니다.'
                }, status=status.HTTP_401_UNAUTHORIZED)

            user_data = response.json()
            oauth_user_id = str(user_data['id'])
            kakao_account = user_data.get('kakao_account', {})

            # 기존 OAuth 프로필 확인
            oauth_profile = OAuthProfile.objects.filter(
                provider='kakao',
                oauth_user_id=oauth_user_id
            ).first()

            if oauth_profile:
                # 기존 사용자 로그인
                login(self.request, oauth_profile.user)
                return Response({
                    'message': '로그인 성공',
                    'user': UserSerializer(oauth_profile.user).data
                })

            # 새 사용자 생성
            user = User.objects.create_user(
                username=f"kakao_{oauth_user_id}",
                email=kakao_account.get('email', ''),
                first_name=kakao_account.get('profile', {}).get('nickname', '')
            )

            # 프로필 생성
            UserProfile.objects.create(user=user)

            # OAuth 프로필 생성
            OAuthProfile.objects.create(
                user=user,
                provider='kakao',
                oauth_user_id=oauth_user_id,
                access_token=access_token,
                expires_at=datetime.now() + timedelta(hours=1)
            )

            login(self.request, user)
            return Response({
                'message': '회원가입 및 로그인 성공',
                'user': UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({
                'message': f'Kakao OAuth 처리 중 오류가 발생했습니다: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
