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
            print(await response.text())

    async def close_session(self) -> None:
        await self.session.close()


class ApiMethods:
    def __init__(self, client: ApiClient):
        self.client = client

    async def __aenter__(self) -> "ApiMethods":
        return self

    async def __aexit__(self, *args) -> None:
        await self.client.close_session()

    # User
    async def get_user(self, tg_user_id: int) -> dict | None:
        return await self.client.request(
            method="GET",
            endpoint=f"/user/{tg_user_id}"
        )

    async def get_users(self) -> dict | None:
        return await self.client.request(
            method="GET",
            endpoint="/user/get_amount"
        )

    async def create_user(self, tg_user_id: int) -> int:
        return await self.client.request(
            method="POST", 
            endpoint="/user/create/", 
            json={"tg_user_id": tg_user_id}
        )
    
    # Post
    async def get_posts_by_tg_user_id(self, tg_user_id: int) -> dict | None:
        return await self.client.request(
            method="GET", 
            endpoint=f"/post/get_posts_by_tg_user_id/{tg_user_id}"
        )
    
    async def get_last_posts(self, tg_user_id: int) -> dict | None:
        return await self.client.request(
            method="GET", 
            endpoint=f"/post/get_last_posts/{tg_user_id}"
        )
    
    async def get_post_by_tg_msg_channel_id(self, tg_msg_channel_id: int) -> dict | None:
        return await self.client.request(
            method="GET", 
            endpoint=f"/post/get_post_by_tg_msg_channel_id/{tg_msg_channel_id}"
        )
    
    async def get_post_by_tg_msg_group_id(self, tg_msg_group_id: int) -> dict | None:
        return await self.client.request(
            method="GET", 
            endpoint=f"/post/get_post_by_tg_msg_group_id/{tg_msg_group_id}"
        )

    async def get_posts(self) -> dict | None:
        return await self.client.request(
            method="GET", 
            endpoint="/post/get_amount/"
        )
    
    async def create_post(self, tg_user_id: int, tg_msg_channel_id: int, feeling_category: str, feeling: str, text: str) -> int:
        return await self.client.request(
            method="POST", 
            endpoint="/post/create/", 
            json={"tg_user_id": tg_user_id, "tg_msg_channel_id": tg_msg_channel_id, "feeling_category": feeling_category, "feeling": feeling, "text": text}
        )
    
    async def delete_post(self, tg_msg_channel_id: int):
        return await self.client.request(
            method="DELETE", 
            endpoint=f"/post/delete/{tg_msg_channel_id}"
        )
    
    async def update_post(self, tg_msg_channel_id: int, tg_msg_group_id: int):
        return await self.client.request(
            method="PUT", 
            endpoint=f"/post/update/{tg_msg_channel_id}/{tg_msg_group_id}"
        )
    
    async def update_post_like_count(self, tg_msg_channel_id: int, like_count: int):
        return await self.client.request(
            method="PUT", 
            endpoint=f"/post/update_like_count/{tg_msg_channel_id}/{like_count}"
        )

    async def update_post_report(self, tg_msg_group_id: int, tg_user_id: int):
        return await self.client.request(
            method="PUT", 
            endpoint=f"/post/update_report/{tg_msg_group_id}/{tg_user_id}"
        )
    
    # Answer
    async def get_answers_by_tg_user_id(self, tg_user_id: int) -> dict | None:
        return await self.client.request(
            method="GET", 
            endpoint=f"/answer/get_answers_by_tg_user_id/{tg_user_id}"
        )
    
    async def get_answer_by_tg_msg_ans_id(self, tg_msg_ans_id: int) -> dict | None:
        return await self.client.request(
            method="GET", 
            endpoint=f"/answer/get_answer_by_tg_msg_ans_id/{tg_msg_ans_id}"
        )
    
    async def create_answer(self, tg_user_id: int, tg_msg_group_id: int, tg_msg_ans_id: int, msg_group_text: str, msg_ans_text: str) -> int:
        return await self.client.request(
            method="POST",
            endpoint="/answer/create/", 
            json={
                "tg_user_id": tg_user_id,
                "tg_msg_group_id": tg_msg_group_id, 
                "tg_msg_ans_id": tg_msg_ans_id,
                "msg_group_text": msg_group_text,
                "msg_ans_text": msg_ans_text
            }
        )

    async def delete_answer(self, tg_msg_ans_id: int, tg_msg_group_id: int):
        return await self.client.request(
            method="DELETE", 
            endpoint=f"/answer/delete/{tg_msg_ans_id}/{tg_msg_group_id}"
        )


client = ApiClient()
methods = ApiMethods(client)