from fastapi import FastAPI
from api.routes.auth import router as auth_router
from api.routes.repos import router as repos_router

app = FastAPI(title="GitHub Cloud Connector")

app.include_router(auth_router)
app.include_router(repos_router)