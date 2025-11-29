#!/usr/bin/env python3
"""
Terminal Color Theme Creator - Web UI

A modern web-based application for creating and exporting terminal color themes.
"""

from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request

from app.api import colors, export

app = FastAPI(title="Terminal Color Theme Creator")

BASE_DIR = Path(__file__).resolve().parent

app.mount("/static", StaticFiles(directory=BASE_DIR / "app" / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "app" / "templates")

app.include_router(colors.router, prefix="/api", tags=["colors"])
app.include_router(export.router, prefix="/api", tags=["export"])


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


def main():
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)


if __name__ == "__main__":
    main()
