"""AI summary / polish / comment generation API endpoints."""

import asyncio

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from app.api.auth import getCurrentUser
from app.core.config import getSettings, Settings
from app.services.ai_service import generateComment, generateSummary, polishContent
from app.services.comment_service import createTargetComment


router = APIRouter(prefix="/ai", tags=["AI"])

CONTENT_MAX_LENGTH = 50000

NIUBAO_USER_ID = 666


class SummaryRequest(BaseModel):
    content: str = Field(min_length=1, max_length=CONTENT_MAX_LENGTH)
    style: str = "formal"
    custom_prompt: str | None = None


class SummaryResponse(BaseModel):
    summary: str
    model: str


class PolishRequest(BaseModel):
    content: str = Field(min_length=1, max_length=CONTENT_MAX_LENGTH)
    style: str = "formatting"
    custom_prompt: str | None = None


class PolishResponse(BaseModel):
    polished: str
    model: str


class CommentRequest(BaseModel):
    content: str = Field(min_length=1, max_length=CONTENT_MAX_LENGTH)
    target_type: str = "article"
    target_id: int


class CommentResponse(BaseModel):
    comment_id: int
    comment_content: str
    model: str


@router.post("/summary", response_model=SummaryResponse)
async def generateArticleSummary(
    request: SummaryRequest,
    currentUser: int = Depends(getCurrentUser),
    settings: Settings = Depends(getSettings),
):
    """Generate an AI-powered summary with style selection."""
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
            style=request.style,
            customPrompt=request.custom_prompt,
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


@router.post("/polish", response_model=PolishResponse)
async def polishArticleContent(
    request: PolishRequest,
    currentUser: int = Depends(getCurrentUser),
    settings: Settings = Depends(getSettings),
):
    """Polish article content with AI."""
    if not settings.ai_api_key:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI service is not configured. Set AI_API_KEY in .env",
        )

    try:
        result = await asyncio.to_thread(
            polishContent,
            content=request.content,
            api_key=settings.ai_api_key,
            base_url=settings.ai_base_url,
            model=settings.ai_model,
            style=request.style,
            customPrompt=request.custom_prompt,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(exc))
    except TimeoutError:
        raise HTTPException(status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                            detail="AI service timed out")
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY,
                            detail=f"AI service error: {exc}")

    return PolishResponse(polished=result["polished"], model=result["model"])


@router.post("/comment", response_model=CommentResponse)
async def generateAiComment(
    request: CommentRequest,
    currentUser: int = Depends(getCurrentUser),
    settings: Settings = Depends(getSettings),
):
    """Generate an AI comment from Niubao and create it."""
    if not settings.ai_api_key:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI service is not configured. Set AI_API_KEY in .env",
        )

    try:
        result = await asyncio.to_thread(
            generateComment,
            content=request.content,
            api_key=settings.ai_api_key,
            base_url=settings.ai_base_url,
            model=settings.ai_model,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(exc))
    except TimeoutError:
        raise HTTPException(status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                            detail="AI service timed out")
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY,
                            detail=f"AI service error: {exc}")

    commentContent = result["comment"]
    commentData = createTargetComment(
        NIUBAO_USER_ID,
        request.target_type,
        request.target_id,
        commentContent,
    )

    if not commentData:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Failed to create AI comment")

    return CommentResponse(
        comment_id=commentData["id"],
        comment_content=commentContent,
        model=result["model"],
    )
