from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.router import apiRouter
from app.core.config import getSettings
from app.db.database import initDatabase


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = getSettings()
    settings.static_dir.mkdir(parents=True, exist_ok=True)
    settings.upload_dir.mkdir(parents=True, exist_ok=True)
    initDatabase()
    yield


def createApp() -> FastAPI:
    settings = getSettings()
    app = FastAPI(title=settings.app_name, lifespan=lifespan)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[settings.frontend_origin, "http://127.0.0.1:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.mount("/static", StaticFiles(directory=settings.static_dir), name="static")
    app.include_router(apiRouter, prefix=settings.api_prefix)

    return app


app = createApp()
