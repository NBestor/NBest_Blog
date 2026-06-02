from pydantic import BaseModel, Field


class QuickNoteRequest(BaseModel):
    content: str = Field(min_length=1, max_length=2000)


class QuickNoteResponse(BaseModel):
    id: int
    user_id: int
    content: str
    create_time: str
    update_time: str


class QuickNoteListResponse(BaseModel):
    items: list[QuickNoteResponse]
