from pydantic import BaseModel, Field


class CalendarEventRequest(BaseModel):
    title: str = Field(min_length=1, max_length=120)
    event_date: str = Field(pattern=r"^\d{4}-\d{2}-\d{2}$")
    event_type: str = Field(default="other", pattern="^(birthday|anniversary|other)$")
    note: str | None = Field(default=None, max_length=1000)
    is_yearly: bool = False


class CalendarEventResponse(BaseModel):
    id: int
    user_id: int
    title: str
    event_date: str
    display_date: str
    event_type: str
    note: str | None
    is_yearly: bool
    create_time: str
    update_time: str


class CalendarEventListResponse(BaseModel):
    items: list[CalendarEventResponse]
