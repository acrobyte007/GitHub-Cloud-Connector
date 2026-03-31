import httpx
from fastapi import HTTPException
from core.config import GITHUB_API_URL


async def fetch_repos(token: str):
    async with httpx.AsyncClient() as client:
        res = await client.get(
            f"{GITHUB_API_URL}/user/repos",
            headers={"Authorization": f"Bearer {token}"}
        )

    if res.status_code != 200:
        raise HTTPException(status_code=res.status_code, detail="Failed to fetch repos")

    return res.json()


async def fetch_issues(token: str, owner: str, repo: str):
    async with httpx.AsyncClient() as client:
        res = await client.get(
            f"{GITHUB_API_URL}/repos/{owner}/{repo}/issues",
            headers={"Authorization": f"Bearer {token}"}
        )

    if res.status_code != 200:
        raise HTTPException(status_code=res.status_code, detail="Failed to fetch issues")

    return res.json()


async def create_issue(token: str, owner: str, repo: str, data: dict):
    async with httpx.AsyncClient() as client:
        res = await client.post(
            f"{GITHUB_API_URL}/repos/{owner}/{repo}/issues",
            headers={"Authorization": f"Bearer {token}"},
            json=data
        )

    if res.status_code not in [200, 201]:
        raise HTTPException(status_code=res.status_code, detail="Failed to create issue")

    return res.json()


async def create_pull_request(token: str, owner: str, repo: str, data: dict):
    async with httpx.AsyncClient() as client:
        res = await client.post(
            f"{GITHUB_API_URL}/repos/{owner}/{repo}/pulls",
            headers={"Authorization": f"Bearer {token}"},
            json=data
        )

    if res.status_code not in [200, 201]:
        raise HTTPException(status_code=res.status_code, detail="Failed to create PR")

    return res.json()


async def fetch_commits(token: str, owner: str, repo: str):
    async with httpx.AsyncClient() as client:
        res = await client.get(
            f"{GITHUB_API_URL}/repos/{owner}/{repo}/commits",
            headers={"Authorization": f"Bearer {token}"}
        )

    if res.status_code != 200:
        raise HTTPException(status_code=res.status_code, detail="Failed to fetch commits")

    return res.json()