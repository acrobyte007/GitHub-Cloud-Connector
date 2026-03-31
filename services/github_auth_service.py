import httpx
from fastapi import HTTPException
from core.config import (
    GITHUB_CLIENT_ID,
    GITHUB_CLIENT_SECRET,
    GITHUB_TOKEN_URL,
    GITHUB_API_URL,
)

user_tokens = {}


async def exchange_code_for_token(code: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            GITHUB_TOKEN_URL,
            headers={"Accept": "application/json"},
            data={
                "client_id": GITHUB_CLIENT_ID,
                "client_secret": GITHUB_CLIENT_SECRET,
                "code": code,
            },
        )

    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Token exchange failed")

    token = response.json().get("access_token")

    if not token:
        raise HTTPException(status_code=400, detail="Invalid token response")

    return token


async def get_github_user(token: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{GITHUB_API_URL}/user",
            headers={"Authorization": f"Bearer {token}"}
        )

    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to fetch user")

    return response.json()