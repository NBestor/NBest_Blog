from pydantic import BaseModel, Field


class TodoRequest(BaseModel):
    title: str = Field(min_length=1, max_length=120)
    content: str | None = Field(default=None, max_length=1000)
    category: str | None = Field(default=None, max_length=40)
    due_date: str | None = Field(default=None, pattern=r"^\d{4}-\d{2}-\d{2}$")


class TodoUpdateRequest(TodoRequest):
    is_done: bool = False


class TodoStatusRequest(BaseModel):
    is_done: bool


class TodoResponse(BaseModel):
    id: int
    user_id: int
    title: str
    content: str | None
    category: str | None
    due_date: str | None
    is_done: bool
    create_time: str
    update_time: str


class TodoListResponse(BaseModel):
    items: list[TodoResponse]
