from pydantic import BaseModel, Field


class RegisterRequest(BaseModel):
    username: str = Field(min_length=3, max_length=32, pattern=r"^[a-zA-Z0-9_-]+$")
    password: str = Field(min_length=6, max_length=64)
    confirm_password: str = Field(min_length=6, max_length=64)
    nickname: str | None = Field(default=None, min_length=1, max_length=32)


class LoginRequest(BaseModel):
    username: str = Field(min_length=3, max_length=32)
    password: str = Field(min_length=6, max_length=64)


class UserResponse(BaseModel):
    id: int
    username: str
    nickname: str
    avatar_url: str | None
    signature: str | None
    role: str
    create_time: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
