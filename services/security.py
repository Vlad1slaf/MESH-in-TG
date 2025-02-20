import aiohttp
from config.settings import settings


class SecurityService:
    async def yandex_auth(self, code: str) -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                    "https://oauth.yandex.ru/token",
                    data={
                        "grant_type": "authorization_code",
                        "code": code,
                        "client_id": settings.YANDEX_CLIENT_ID,
                        "client_secret": settings.YANDEX_CLIENT_SECRET
                    }
            ) as resp:
                token_data = await resp.json()

            async with session.get(
                    "https://login.yandex.ru/info",
                    headers={"Authorization": f"OAuth {token_data['access_token']}"}
            ) as resp:
                return await resp.json()