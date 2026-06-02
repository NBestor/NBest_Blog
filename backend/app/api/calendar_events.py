from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.api.auth import getCurrentUser
from app.schemas.calendar_event import CalendarEventListResponse, CalendarEventRequest, CalendarEventResponse
from app.services.calendar_event_service import (
    createCalendarEvent,
    deleteCalendarEvent,
    listCalendarEvents,
    listCalendarReminders,
    updateCalendarEvent,
)


router = APIRouter(prefix="/calendar-events", tags=["calendar-events"])


@router.get("", response_model=CalendarEventListResponse)
def getCalendarEvents(
    month: str | None = Query(default=None, pattern=r"^\d{4}-\d{2}$"),
    currentUser: dict[str, str | int | None] = Depends(getCurrentUser),
) -> CalendarEventListResponse:
    return CalendarEventListResponse(items=listCalendarEvents(int(currentUser["id"]), month))


@router.get("/reminders", response_model=CalendarEventListResponse)
def getCalendarEventReminders(
    currentUser: dict[str, str | int | None] = Depends(getCurrentUser),
) -> CalendarEventListResponse:
    return CalendarEventListResponse(items=listCalendarReminders(int(currentUser["id"])))


@router.post("", response_model=CalendarEventResponse, status_code=status.HTTP_201_CREATED)
def createCalendarEventEndpoint(
    request: CalendarEventRequest,
    currentUser: dict[str, str | int | None] = Depends(getCurrentUser),
) -> CalendarEventResponse:
    return CalendarEventResponse(
        **createCalendarEvent(
            int(currentUser["id"]),
            request.title,
            request.event_date,
            request.event_type,
            request.note,
            request.is_yearly,
        )
    )


@router.put("/{event_id}", response_model=CalendarEventResponse)
def updateCalendarEventEndpoint(
    event_id: int,
    request: CalendarEventRequest,
    currentUser: dict[str, str | int | None] = Depends(getCurrentUser),
) -> CalendarEventResponse:
    event = updateCalendarEvent(
        int(currentUser["id"]),
        event_id,
        request.title,
        request.event_date,
        request.event_type,
        request.note,
        request.is_yearly,
    )
    if event is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Calendar event not found")
    return CalendarEventResponse(**event)


@router.delete("/{event_id}")
def deleteCalendarEventEndpoint(
    event_id: int,
    currentUser: dict[str, str | int | None] = Depends(getCurrentUser),
) -> dict[str, str]:
    isDeleted = deleteCalendarEvent(int(currentUser["id"]), event_id)
    if not isDeleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Calendar event not found")
    return {"status": "ok"}
