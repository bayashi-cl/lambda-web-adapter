from typing import Literal

import httpx
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI()


class CheckResponse(BaseModel):
    status: Literal["ok"] = "ok"


@app.get("/check")
def check() -> CheckResponse:
    return CheckResponse()


class AppResponse(BaseModel):
    message: str


@app.get("/app")
def app_() -> AppResponse:
    resp = httpx.post(
        "http://localhost:9000/2015-03-31/functions/function/invocations",
        json={"question": "aaa"},
        timeout=5,
    ).raise_for_status()
    print(resp.status_code)
    print(resp.json())
    return AppResponse(message=resp.json()["answer"])


# app.mount("/static", StaticFiles(directory="static", html=True), name="static")


# @app.get("/")
# def root() -> RedirectResponse:
#     return RedirectResponse("/static")
