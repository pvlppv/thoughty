import aiohttp
from settings import get_settings

cfg = get_settings()

class ApiClient:
    def __init__(self):
        self.session = aiohttp.ClientSession(base_url=cfg.url)

    async def request(self, method: str, endpoint: str, **kwargs) -> aiohttp.ClientResponse:
        async with self.session.request(method=method, url=endpoint, **kwargs) as response:
            if response.status == 200:
                return await response.json()

    async def close_session(self) -> None:
        await self.session.close()


class ApiMethods:
    def __init__(self, client: ApiClient):
        self.client = client

    async def __aenter__(self) -> "ApiMethods":
        return self

    async def __aexit__(self, *args) -> None:
        await self.client.close_session()

    async def get_user(self, telegram_id: int) -> dict | None:
        return await self.client.request(
            method="GET",
            endpoint=f"/user/{telegram_id}/"
        )

    async def get_users(self) -> dict | None:
        return await self.client.request(
            method="GET",
            endpoint="/user/get_amount/"
        )

    async def create_user(self, telegram_id: int) -> int:
        return await self.client.request(
            method="POST", 
            endpoint="/user/create/", 
            json={"telegram_id": telegram_id}
        )
    

    async def get_posts_by_tg_user_id(self, telegram_user_id: int) -> dict | None:
        return await self.client.request(
            method="GET", 
            endpoint=f"/post/get/{telegram_user_id}"
        )

    async def get_posts(self) -> dict | None:
        return await self.client.request(
            method="GET", 
            endpoint="/post/get_amount/"
        )
    
    async def create_post(self, telegram_user_id: int, telegram_message_id: int, mood: str, text: str) -> int:
        return await self.client.request(
            method="POST", 
            endpoint="/post/create/", 
            json={"telegram_user_id": telegram_user_id, "telegram_message_id": telegram_message_id, "mood": mood, "text": text}
        )
    
    async def delete_post(self, telegram_message_id: int):
        return await self.client.request(
            method="DELETE", 
            endpoint=f"/post/delete/{telegram_message_id}"
        )


client = ApiClient()
methods = ApiMethods(client)