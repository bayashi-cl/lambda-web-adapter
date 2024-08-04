from pathlib import Path
from typing import Literal

import httpx
from fastapi import APIRouter, FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    STATIC_PATH: Path = Field(default=...)

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)


settings = Settings()

app = FastAPI(root_path="/prod")
router = APIRouter()


class CheckResponse(BaseModel):
    status: Literal["ok"]


@router.get("/check")
def check() -> CheckResponse:
    return CheckResponse(status="ok")


class AppResponse(BaseModel):
    message: str


@router.get("/app")
def app_() -> AppResponse:
    resp = httpx.post(
        "http://localhost:9000/2015-03-31/functions/function/invocations",
        json={"question": "aaa"},
        timeout=5,
    ).raise_for_status()
    print(resp.status_code)
    print(resp.json())
    return AppResponse(message=resp.json()["answer"])


app.include_router(router, prefix="/api")
app.mount("/", StaticFiles(directory=settings.STATIC_PATH, html=True))
