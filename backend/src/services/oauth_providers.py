import httpx
from typing import Optional, Dict, Any
from config.settings import settings

class OAuthProviderBase:
    def __init__(self, client_id: str, client_secret: str, redirect_uri: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
    
    async def get_auth_url(self, state: str) -> str:
        raise NotImplementedError
    
    async def get_tokens(self, code: str) -> Dict[str, Any]:
        raise NotImplementedError
    
    async def get_user_info(self, access_token: str) -> Dict[str, Any]:
        raise NotImplementedError

class GoogleOAuth(OAuthProviderBase):
    AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
    TOKEN_URL = "https://oauth2.googleapis.com/token"
    USER_INFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"
    SCOPE = "openid profile email"
    
    async def get_auth_url(self, state: str) -> str:
        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "response_type": "code",
            "scope": self.SCOPE,
            "state": state,
            "access_type": "offline"
        }
        query_string = "&".join([f"{k}={v}" for k, v in params.items()])
        return f"{self.AUTH_URL}?{query_string}"
    
    async def get_tokens(self, code: str) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.TOKEN_URL,
                data={
                    "code": code,
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "redirect_uri": self.redirect_uri,
                    "grant_type": "authorization_code"
                }
            )
            return response.json()
    
    async def get_user_info(self, access_token: str) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                self.USER_INFO_URL,
                headers={"Authorization": f"Bearer {access_token}"}
            )
            return response.json()

class YandexOAuth(OAuthProviderBase):
    AUTH_URL = "https://oauth.yandex.com/authorize"
    TOKEN_URL = "https://oauth.yandex.com/token"
    USER_INFO_URL = "https://login.yandex.ru/info"
    SCOPE = "login:email login:info"
    
    async def get_auth_url(self, state: str) -> str:
        params = {
            "client_id": self.client_id,
            "response_type": "code",
            "state": state
        }
        query_string = "&".join([f"{k}={v}" for k, v in params.items()])
        return f"{self.AUTH_URL}?{query_string}"
    
    async def get_tokens(self, code: str) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.TOKEN_URL,
                data={
                    "grant_type": "authorization_code",
                    "code": code,
                    "client_id": self.client_id,
                    "client_secret": self.client_secret
                }
            )
            return response.json()
    
    async def get_user_info(self, access_token: str) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                self.USER_INFO_URL,
                headers={"Authorization": f"OAuth {access_token}"}
            )
            return response.json()

class VKOAuth(OAuthProviderBase):
    AUTH_URL = "https://oauth.vk.com/authorize"
    TOKEN_URL = "https://oauth.vk.com/access_token"
    USER_INFO_URL = "https://api.vk.com/method/users.get"
    API_VERSION = "5.131"
    
    async def get_auth_url(self, state: str) -> str:
        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "scope": "email",
            "response_type": "code",
            "state": state,
            "v": self.API_VERSION
        }
        query_string = "&".join([f"{k}={v}" for k, v in params.items()])
        return f"{self.AUTH_URL}?{query_string}"
    
    async def get_tokens(self, code: str) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.TOKEN_URL,
                data={
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "code": code,
                    "redirect_uri": self.redirect_uri
                }
            )
            return response.json()
    
    async def get_user_info(self, access_token: str) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                self.USER_INFO_URL,
                params={
                    "access_token": access_token,
                    "fields": "photo_max,domain,first_name,last_name,email",
                    "v": self.API_VERSION
                }
            )
            data = response.json()
            if "response" in data and len(data["response"]) > 0:
                return data["response"][0]
            return data

def get_oauth_provider(provider: str, redirect_uri: str) -> Optional[OAuthProviderBase]:
    """Factory function to get OAuth provider instance"""
    providers = {
        "google": (
            GoogleOAuth,
            settings.GOOGLE_CLIENT_ID,
            settings.GOOGLE_CLIENT_SECRET
        ),
        "yandex": (
            YandexOAuth,
            settings.YANDEX_CLIENT_ID,
            settings.YANDEX_CLIENT_SECRET
        ),
        "vk": (
            VKOAuth,
            settings.GITHUB_CLIENT_ID,  # Placeholder
            settings.GITHUB_CLIENT_SECRET  # Placeholder
        )
    }
    
    if provider not in providers:
        return None
    
    provider_class, client_id, client_secret = providers[provider]
    return provider_class(client_id, client_secret, redirect_uri)
