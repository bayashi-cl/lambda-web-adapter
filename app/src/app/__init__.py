from typing import Literal

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class RootResponse(BaseModel):
    status: Literal["ok"] = "ok"


@app.get("/")
def root() -> RootResponse:
    return RootResponse()
