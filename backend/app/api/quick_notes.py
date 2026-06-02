from fastapi import APIRouter, Depends, HTTPException, status

from app.api.auth import getCurrentUser
from app.schemas.quick_note import QuickNoteListResponse, QuickNoteRequest, QuickNoteResponse
from app.services.quick_note_service import createQuickNote, deleteQuickNote, listQuickNotes


router = APIRouter(prefix="/quick-notes", tags=["quick-notes"])


@router.get("", response_model=QuickNoteListResponse)
def getQuickNotes(currentUser: dict[str, str | int | None] = Depends(getCurrentUser)) -> QuickNoteListResponse:
    return QuickNoteListResponse(items=listQuickNotes(int(currentUser["id"])))


@router.post("", response_model=QuickNoteResponse, status_code=status.HTTP_201_CREATED)
def createQuickNoteEndpoint(
    request: QuickNoteRequest,
    currentUser: dict[str, str | int | None] = Depends(getCurrentUser),
) -> QuickNoteResponse:
    return QuickNoteResponse(**createQuickNote(int(currentUser["id"]), request.content))


@router.delete("/{quick_note_id}")
def deleteQuickNoteEndpoint(
    quick_note_id: int,
    currentUser: dict[str, str | int | None] = Depends(getCurrentUser),
) -> dict[str, str]:
    isDeleted = deleteQuickNote(int(currentUser["id"]), quick_note_id)
    if not isDeleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quick note not found")
    return {"status": "ok"}
