import httpx
from core.config import (
    CLIENT_ID,
    CLIENT_SECRET,
    GITHUB_TOKEN_URL,
    GITHUB_API_URL,
)

# Temporary in-memory storage 
user_tokens = {}


async def exchange_code_for_token(code: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            GITHUB_TOKEN_URL,
            headers={"Accept": "application/json"},
            data={
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "code": code,
            },
        )

    data = response.json()
    return data.get("access_token")


async def get_github_user(token: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{GITHUB_API_URL}/user",
            headers={"Authorization": f"Bearer {token}"},
        )

    return response.json()