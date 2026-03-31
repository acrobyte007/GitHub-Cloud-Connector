from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from core.config import GITHUB_CLIENT_ID, GITHUB_AUTHORIZE_URL, REDIRECT_URI
from services.github_auth_service import (
    exchange_code_for_token,
    get_github_user,
    user_tokens,
)

router = APIRouter(prefix="/auth/github", tags=["Auth"])


class UserResponse(BaseModel):
    id: int
    login: str
    name: str | None
    public_repos: int


class AuthResponse(BaseModel):
    message: str
    user_id: int


@router.get("/login")
async def github_login():
    url = (
        f"{GITHUB_AUTHORIZE_URL}"
        f"?client_id={GITHUB_CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
    )
    return RedirectResponse(url)


@router.get("/callback", response_model=AuthResponse)
async def github_callback(code: str):
    token = await exchange_code_for_token(code)
    user = await get_github_user(token)

    user_id = user["id"]
    user_tokens[user_id] = token

    return AuthResponse(message="Connected successfully", user_id=user_id)


@router.get("/me/{user_id}", response_model=UserResponse)
async def get_me(user_id: int):
    token = user_tokens.get(user_id)

    if not token:
        raise HTTPException(status_code=404, detail="User not found")

    user = await get_github_user(token)

    return UserResponse(
        id=user["id"],
        login=user["login"],
        name=user.get("name"),
        public_repos=user["public_repos"]
    )