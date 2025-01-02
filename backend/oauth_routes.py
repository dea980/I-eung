from fastapi import APIRouter, HTTPException, Request
from typing import Optional
import httpx
from .oauth_config import OAuthConfig

router = APIRouter()

@router.post("/oauth/{provider}/callback")
async def oauth_callback(provider: str, code: str, request: Request):
    try:
        config = OAuthConfig.get_provider_config(provider)
        base_url = str(request.base_url)
        
        # Get access token
        token_data = await get_access_token(provider, code, config, base_url)
        
        # Get user info
        user_info = await get_user_info(provider, token_data["access_token"], config)
        
        # Create or update user
        user = await create_or_update_user(provider, user_info)
        
        return {
            "access_token": token_data["access_token"],
            "token_type": "bearer",
            "user": user
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"OAuth error: {str(e)}")

async def get_access_token(provider: str, code: str, config: dict, base_url: str) -> dict:
    async with httpx.AsyncClient() as client:
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "client_id": config["client_id"],
            "client_secret": config["client_secret"],
            "redirect_uri": OAuthConfig.get_redirect_uri(provider, base_url)
        }
        
        response = await client.post(config["token_url"], data=data)
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to get access token")
        
        return response.json()

async def get_user_info(provider: str, access_token: str, config: dict) -> dict:
    async with httpx.AsyncClient() as client:
        headers = {"Authorization": f"Bearer {access_token}"}
        
        # Provider-specific adjustments
        if provider == "naver":
            response = await client.get(config["userinfo_url"], headers=headers)
            data = response.json()
            return data["response"]
        elif provider == "kakao":
            response = await client.get(config["userinfo_url"], headers=headers)
            data = response.json()
            return {
                "id": str(data["id"]),
                "email": data["kakao_account"].get("email"),
                "name": data["kakao_account"]["profile"].get("nickname"),
                "profile_image": data["kakao_account"]["profile"].get("profile_image_url")
            }
        elif provider == "meta":
            response = await client.get(
                config["userinfo_url"],
                headers=headers,
                params={"fields": "id,name,email,picture"}
            )
            data = response.json()
            return {
                "id": data["id"],
                "email": data.get("email"),
                "name": data.get("name"),
                "profile_image": data.get("picture", {}).get("data", {}).get("url")
            }
        else:  # Google
            response = await client.get(config["userinfo_url"], headers=headers)
            data = response.json()
            return {
                "id": data["sub"],
                "email": data["email"],
                "name": data["name"],
                "profile_image": data.get("picture")
            }

async def create_or_update_user(provider: str, user_info: dict) -> dict:
    # TODO: Implement user creation/update in own database
    # This is a placeholder that returns the user info as-is
    return {
        "id": user_info["id"],
        "email": user_info["email"],
        "name": user_info["name"],
        "profile_image": user_info.get("profile_image"),
        "oauth_provider": provider
    }