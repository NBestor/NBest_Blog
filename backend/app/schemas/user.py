from pydantic import BaseModel, Field


class ProfileUpdateRequest(BaseModel):
    nickname: str = Field(min_length=1, max_length=32)
    signature: str | None = Field(default=None, max_length=120)


class PasswordUpdateRequest(BaseModel):
    old_password: str = Field(min_length=6, max_length=64)
    new_password: str = Field(min_length=6, max_length=64)
    confirm_password: str = Field(min_length=6, max_length=64)
