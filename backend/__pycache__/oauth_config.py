from typing import Dict, Optional
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config

# OAuth configuration
config = Config('.env')

oauth = OAuth()
 ## OAuth configuration for Starlette
# Google OAuth
oauth.register(
    name='google',
    client_id=config('GOOGLE_CLIENT_ID', default=''),
    client_secret=config('GOOGLE_CLIENT_SECRET', default=''),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)

# Apple OAuth
oauth.register(
    name='apple',
    client_id=config('APPLE_CLIENT_ID', default=''),
    client_secret=config('APPLE_CLIENT_SECRET', default=''),
    authorize_url='https://appleid.apple.com/auth/authorize',
    authorize_params={'response_mode': 'form_post'},
    access_token_url='https://appleid.apple.com/auth/token',
    client_kwargs={'scope': 'name email'}
)

# Kakao OAuth
oauth.register(
    name='kakao',
    client_id=config('KAKAO_CLIENT_ID', default=''),
    client_secret=config('KAKAO_CLIENT_SECRET', default=''),
    authorize_url='https://kauth.kakao.com/oauth/authorize',
    authorize_params={},
    access_token_url='https://kauth.kakao.com/oauth/token',
    api_base_url='https://kapi.kakao.com/v2/user/me',
    client_kwargs={'scope': 'profile_nickname profile_image account_email'}
)

# Naver OAuth
oauth.register(
    name='naver',
    client_id=config('NAVER_CLIENT_ID', default=''),
    client_secret=config('NAVER_CLIENT_SECRET', default=''),
    authorize_url='https://nid.naver.com/oauth2.0/authorize',
    authorize_params={},
    access_token_url='https://nid.naver.com/oauth2.0/token',
    api_base_url='https://openapi.naver.com/v1/nid/me',
    client_kwargs={'scope': 'name email profile_image'}
)

# Provider specific user info extractors
def extract_google_user(token_response: Dict) -> Dict:
    return {
        'email': token_response.get('email'),
        'name': token_response.get('name'),
        'picture': token_response.get('picture'),
        'provider': 'google'
    }

def extract_apple_user(token_response: Dict) -> Dict:
    return {
        'email': token_response.get('email'),
        'name': token_response.get('name', {}).get('firstName', ''),
        'provider': 'apple'
    }

def extract_kakao_user(token_response: Dict) -> Dict:
    account = token_response.get('kakao_account', {})
    profile = account.get('profile', {})
    return {
        'email': account.get('email'),
        'name': profile.get('nickname'),
        'picture': profile.get('profile_image_url'),
        'provider': 'kakao'
    }

def extract_naver_user(token_response: Dict) -> Dict:
    response = token_response.get('response', {})
    return {
        'email': response.get('email'),
        'name': response.get('name'),
        'picture': response.get('profile_image'),
        'provider': 'naver'
    }

# Map of providers to their user info extractors
user_info_extractors = {
    'google': extract_google_user,
    'apple': extract_apple_user,
    'kakao': extract_kakao_user,
    'naver': extract_naver_user
}