"""AI summary generation API endpoints."""

import asyncio

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from app.api.auth import getCurrentUser
from app.core.config import getSettings, Settings
from app.services.ai_service import generateSummary


router = APIRouter(prefix="/ai", tags=["AI"])

CONTENT_MAX_LENGTH = 50000


class SummaryRequest(BaseModel):
    content: str = Field(min_length=1, max_length=CONTENT_MAX_LENGTH)


class SummaryResponse(BaseModel):
    summary: str
    model: str


@router.post("/summary", response_model=SummaryResponse)
async def generateArticleSummary(
    request: SummaryRequest,
    currentUser: int = Depends(getCurrentUser),
    settings: Settings = Depends(getSettings),
):
    """Generate an AI-powered summary for article content."""
    if not settings.ai_api_key:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI service is not configured. Set AI_API_KEY in .env",
        )

    try:
        result = await asyncio.to_thread(
            generateSummary,
            content=request.content,
            api_key=settings.ai_api_key,
            base_url=settings.ai_base_url,
            model=settings.ai_model,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        )
    except TimeoutError:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="AI service timed out, please try again",
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"AI service error: {exc}",
        )

    return SummaryResponse(summary=result["summary"], model=result["model"])