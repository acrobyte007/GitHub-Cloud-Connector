from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
from core.config import CLIENT_ID, REDIRECT_URI, GITHUB_AUTH_URL
from services.github_auth_service import (
    exchange_code_for_token,
    get_github_user,
    user_tokens,
)

router = APIRouter()


@router.get("/auth/github/login")
def github_login():
    url = (
        f"{GITHUB_AUTH_URL}"
        f"?client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&scope=repo"
    )
    return RedirectResponse(url)





@router.get("/auth/github/callback")
async def github_callback(code: str):
    token = await exchange_code_for_token(code)

    if not token:
        raise HTTPException(status_code=400, detail="Token exchange failed")

    user_data = await get_github_user(token)
    github_id = user_data.get("id")

    user_tokens[github_id] = token

    return RedirectResponse(
        url=f"/success?user_id={github_id}"
    )


@router.get("/auth/github/me")
async def get_me(github_user_id: int):
    token = user_tokens.get(github_user_id)

    if not token:
        raise HTTPException(status_code=404, detail="User not connected")

    user_data = await get_github_user(token)

    return user_data


@router.get("/success")
def success(user_id: int):
    return {
        "message": "GitHub connected successfully",
        "github_user_id": user_id
    }