from pydantic import BaseModel


class FollowUserResponse(BaseModel):
    id: int
    username: str
    nickname: str
    avatar_url: str | None
    signature: str | None
    role: str
    create_time: str
    is_following: bool = False
    is_friend: bool = False


class FollowListResponse(BaseModel):
    items: list[FollowUserResponse]
