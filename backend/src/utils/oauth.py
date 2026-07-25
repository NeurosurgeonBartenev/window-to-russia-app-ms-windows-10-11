"""
OAuth utilities for handling OAuth 2.0 flows
"""

import aiohttp
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)


class OAuthProvider:
    """
    Base OAuth provider class
    """
    
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        redirect_uri: str
    ):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
    
    async def get_authorization_url(self, state: str) -> str:
        """
        Get OAuth authorization URL
        """
        raise NotImplementedError
    
    async def exchange_code_for_token(self, code: str) -> Optional[Dict[str, Any]]:
        """
        Exchange authorization code for access token
        """
        raise NotImplementedError
    
    async def get_user_info(self, access_token: str) -> Optional[Dict[str, Any]]:
        """
        Get user information from OAuth provider
        """
        raise NotImplementedError


class GoogleOAuthProvider(OAuthProvider):
    """
    Google OAuth provider
    """
    
    AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
    TOKEN_URL = "https://oauth2.googleapis.com/token"
    USER_INFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"
    
    async def get_authorization_url(self, state: str) -> str:
        """
        Get Google OAuth authorization URL
        """
        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "response_type": "code",
            "scope": "openid email profile",
            "state": state,
            "access_type": "offline"
        }
        query_string = "&".join([f"{k}={v}" for k, v in params.items()])
        return f"{self.AUTH_URL}?{query_string}"
    
    async def exchange_code_for_token(self, code: str) -> Optional[Dict[str, Any]]:
        """
        Exchange authorization code for access token
        """
        data = {
            "code": code,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "redirect_uri": self.redirect_uri,
            "grant_type": "authorization_code"
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(self.TOKEN_URL, data=data) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    logger.error(f"Failed to exchange code: {await response.text()}")
                    return None
    
    async def get_user_info(self, access_token: str) -> Optional[Dict[str, Any]]:
        """
        Get user information from Google
        """
        headers = {"Authorization": f"Bearer {access_token}"}
        
        async with aiohttp.ClientSession() as session:
            async with session.get(self.USER_INFO_URL, headers=headers) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    logger.error(f"Failed to get user info: {await response.text()}")
                    return None


class YandexOAuthProvider(OAuthProvider):
    """
    Yandex OAuth provider
    """
    
    AUTH_URL = "https://oauth.yandex.com/authorize"
    TOKEN_URL = "https://oauth.yandex.com/token"
    USER_INFO_URL = "https://login.yandex.ru/info"
    
    async def get_authorization_url(self, state: str) -> str:
        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "response_type": "code",
            "state": state,
            "force_confirm": "yes"
        }
        query_string = "&".join([f"{k}={v}" for k, v in params.items()])
        return f"{self.AUTH_URL}?{query_string}"
    
    async def exchange_code_for_token(self, code: str) -> Optional[Dict[str, Any]]:
        data = {
            "code": code,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "authorization_code"
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(self.TOKEN_URL, data=data) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    logger.error(f"Failed to exchange code: {await response.text()}")
                    return None
    
    async def get_user_info(self, access_token: str) -> Optional[Dict[str, Any]]:
        headers = {"Authorization": f"OAuth {access_token}"}
        
        async with aiohttp.ClientSession() as session:
            async with session.get(self.USER_INFO_URL, headers=headers) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    logger.error(f"Failed to get user info: {await response.text()}")
                    return None


# OAuth providers registry
OAUTH_PROVIDERS = {
    "google": GoogleOAuthProvider,
    "yandex": YandexOAuthProvider,
    # Additional providers would be added here (vk, microsoft, apple, etc.)
}


def get_oauth_provider(provider_name: str) -> Optional[OAuthProvider]:
    """
    Get OAuth provider by name
    """
    provider_class = OAUTH_PROVIDERS.get(provider_name.lower())
    if not provider_class:
        return None
    
    settings_map = {
        "google": ("GOOGLE_CLIENT_ID", "GOOGLE_CLIENT_SECRET", "GOOGLE_REDIRECT_URI"),
        "yandex": ("YANDEX_CLIENT_ID", "YANDEX_CLIENT_SECRET", "YANDEX_REDIRECT_URI"),
    }
    
    if provider_name.lower() not in settings_map:
        return None
    
    client_id_key, client_secret_key, redirect_uri_key = settings_map[provider_name.lower()]
    
    from src.config.settings import settings
    
    client_id = getattr(settings, client_id_key, "")
    client_secret = getattr(settings, client_secret_key, "")
    redirect_uri = getattr(settings, redirect_uri_key, "")
    
    if not all([client_id, client_secret, redirect_uri]):
        logger.warning(f"OAuth provider {provider_name} not fully configured")
        return None
    
    return provider_class(client_id, client_secret, redirect_uri)
