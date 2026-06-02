from fastapi import APIRouter

from app.core.config import getSettings
from app.db.database import canConnectDatabase


router = APIRouter(prefix="/health", tags=["health"])


@router.get("")
def getHealth() -> dict[str, str | bool]:
    settings = getSettings()
    return {
        "appName": settings.app_name,
        "status": "ok",
        "databaseConnected": canConnectDatabase(),
    }
