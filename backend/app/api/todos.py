from fastapi import APIRouter, Depends, HTTPException, status

from app.api.auth import getCurrentUser
from app.schemas.todo import TodoListResponse, TodoRequest, TodoResponse, TodoStatusRequest, TodoUpdateRequest
from app.services.todo_service import (
    createTodo,
    deleteTodo,
    listTodoReminders,
    listTodos,
    setTodoDone,
    updateTodo,
)


router = APIRouter(prefix="/todos", tags=["todos"])


@router.get("", response_model=TodoListResponse)
def getTodos(currentUser: dict[str, str | int | None] = Depends(getCurrentUser)) -> TodoListResponse:
    return TodoListResponse(items=listTodos(int(currentUser["id"])))


@router.get("/reminders", response_model=TodoListResponse)
def getTodoReminders(currentUser: dict[str, str | int | None] = Depends(getCurrentUser)) -> TodoListResponse:
    return TodoListResponse(items=listTodoReminders(int(currentUser["id"])))


@router.post("", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
def createTodoEndpoint(
    request: TodoRequest,
    currentUser: dict[str, str | int | None] = Depends(getCurrentUser),
) -> TodoResponse:
    return TodoResponse(
        **createTodo(int(currentUser["id"]), request.title, request.content, request.category, request.due_date)
    )


@router.put("/{todo_id}", response_model=TodoResponse)
def updateTodoEndpoint(
    todo_id: int,
    request: TodoUpdateRequest,
    currentUser: dict[str, str | int | None] = Depends(getCurrentUser),
) -> TodoResponse:
    todo = updateTodo(
        int(currentUser["id"]),
        todo_id,
        request.title,
        request.content,
        request.category,
        request.due_date,
        request.is_done,
    )
    if todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    return TodoResponse(**todo)


@router.patch("/{todo_id}/status", response_model=TodoResponse)
def updateTodoStatusEndpoint(
    todo_id: int,
    request: TodoStatusRequest,
    currentUser: dict[str, str | int | None] = Depends(getCurrentUser),
) -> TodoResponse:
    todo = setTodoDone(int(currentUser["id"]), todo_id, request.is_done)
    if todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    return TodoResponse(**todo)


@router.delete("/{todo_id}")
def deleteTodoEndpoint(
    todo_id: int,
    currentUser: dict[str, str | int | None] = Depends(getCurrentUser),
) -> dict[str, str]:
    isDeleted = deleteTodo(int(currentUser["id"]), todo_id)
    if not isDeleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    return {"status": "ok"}
