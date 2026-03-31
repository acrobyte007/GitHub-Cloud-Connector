from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from services.github_auth_service import user_tokens
from services.github_service import (
    fetch_repos,
    fetch_issues,
    create_issue,
    create_pull_request,
    fetch_commits
)

router = APIRouter(tags=["Repositories"])


class RepoResponse(BaseModel):
    name: str
    private: bool
    stars: int
    url: str


class IssueCreate(BaseModel):
    title: str
    body: str | None = None


class IssueResponse(BaseModel):
    title: str
    state: str
    created_at: str
    url: str


class PRCreate(BaseModel):
    title: str
    head: str
    base: str
    body: str | None = None


class PRResponse(BaseModel):
    title: str
    state: str
    url: str


class CommitResponse(BaseModel):
    message: str
    author: str
    date: str
    url: str


@router.get("/users/{user_id}/repos", response_model=List[RepoResponse])
async def get_repos(user_id: int):
    token = user_tokens.get(user_id)

    if not token:
        raise HTTPException(status_code=404, detail="User not connected")

    repos = await fetch_repos(token)

    return [
        RepoResponse(
            name=r["name"],
            private=r["private"],
            stars=r["stargazers_count"],
            url=r["html_url"]
        )
        for r in repos
    ]


@router.get("/repos/{user_id}/{owner}/{repo}/issues", response_model=List[IssueResponse])
async def list_issues(user_id: int, owner: str, repo: str):
    token = user_tokens.get(user_id)

    if not token:
        raise HTTPException(status_code=404, detail="User not connected")

    issues = await fetch_issues(token, owner, repo)

    return [
        IssueResponse(
            title=i["title"],
            state=i["state"],
            created_at=i["created_at"],
            url=i["html_url"]
        )
        for i in issues if "pull_request" not in i
    ]


@router.post("/repos/{user_id}/{owner}/{repo}/issues", response_model=IssueResponse)
async def create_new_issue(user_id: int, owner: str, repo: str, payload: IssueCreate):
    token = user_tokens.get(user_id)

    if not token:
        raise HTTPException(status_code=404, detail="User not connected")

    issue = await create_issue(token, owner, repo, payload.dict())

    return IssueResponse(
        title=issue["title"],
        state=issue["state"],
        created_at=issue["created_at"],
        url=issue["html_url"]
    )


@router.post("/repos/{user_id}/{owner}/{repo}/pulls", response_model=PRResponse)
async def create_pr(user_id: int, owner: str, repo: str, payload: PRCreate):
    token = user_tokens.get(user_id)

    if not token:
        raise HTTPException(status_code=404, detail="User not connected")

    pr = await create_pull_request(token, owner, repo, payload.dict())

    return PRResponse(
        title=pr["title"],
        state=pr["state"],
        url=pr["html_url"]
    )


@router.get("/repos/{user_id}/{owner}/{repo}/commits", response_model=List[CommitResponse])
async def get_commits(user_id: int, owner: str, repo: str):
    token = user_tokens.get(user_id)

    if not token:
        raise HTTPException(status_code=404, detail="User not connected")

    commits = await fetch_commits(token, owner, repo)

    return [
        CommitResponse(
            message=c["commit"]["message"],
            author=c["commit"]["author"]["name"],
            date=c["commit"]["author"]["date"],
            url=c["html_url"]
        )
        for c in commits
    ]