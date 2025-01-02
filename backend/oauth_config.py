from typing import Dict, Any
import os
from dotenv import load_dotenv

load_dotenv()

class OAuthConfig:
    PROVIDERS = {
        'google': {
            'auth_url': 'https://accounts.google.com/o/oauth2/v2/auth',
            'token_url': 'https://oauth2.googleapis.com/token',
            'userinfo_url': 'https://www.googleapis.com/oauth2/v3/userinfo',
            'client_id': os.getenv('GOOGLE_CLIENT_ID'),
            'client_secret': os.getenv('GOOGLE_CLIENT_SECRET'),
            'scope': 'email profile',
        },
        'naver': {
            'auth_url': 'https://nid.naver.com/oauth2.0/authorize',
            'token_url': 'https://nid.naver.com/oauth2.0/token',
            'userinfo_url': 'https://openapi.naver.com/v1/nid/me',
            'client_id': os.getenv('NAVER_CLIENT_ID'),
            'client_secret': os.getenv('NAVER_CLIENT_SECRET'),
            'scope': 'name email profile',
        },
        'kakao': {
            'auth_url': 'https://kauth.kakao.com/oauth/authorize',
            'token_url': 'https://kauth.kakao.com/oauth/token',
            'userinfo_url': 'https://kapi.kakao.com/v2/user/me',
            'client_id': os.getenv('KAKAO_CLIENT_ID'),
            'client_secret': os.getenv('KAKAO_CLIENT_SECRET'),
            'scope': 'profile_nickname account_email profile_image',
        },
        'meta': {
            'auth_url': 'https://www.facebook.com/v12.0/dialog/oauth',
            'token_url': 'https://graph.facebook.com/v12.0/oauth/access_token',
            'userinfo_url': 'https://graph.facebook.com/me',
            'client_id': os.getenv('META_CLIENT_ID'),
            'client_secret': os.getenv('META_CLIENT_SECRET'),
            'scope': 'email public_profile',
        }
    }

    @staticmethod
    def get_provider_config(provider: str) -> Dict[str, Any]:
        if provider not in OAuthConfig.PROVIDERS:
            raise ValueError(f"Unsupported OAuth provider: {provider}")
        return OAuthConfig.PROVIDERS[provider]

    @staticmethod
    def get_redirect_uri(provider: str, base_url: str) -> str:
        return f"{base_url}/api/oauth/{provider}/callback"