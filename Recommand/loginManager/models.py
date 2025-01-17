from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    """
    사용자 프로필 모델
    기본 Django User 모델을 확장하여 추가 정보를 저장
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    nickname = models.CharField(max_length=50, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s profile"

class OAuthProfile(models.Model):
    """
    OAuth 프로필 정보를 저장하는 모델
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='oauth_profiles')
    provider = models.CharField(max_length=20)  # 'google', 'kakao', etc.
    oauth_user_id = models.CharField(max_length=100)
    access_token = models.TextField()
    refresh_token = models.TextField(blank=True, null=True)
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('provider', 'oauth_user_id')

    def __str__(self):
        return f"{self.user.username}'s {self.provider} profile"
