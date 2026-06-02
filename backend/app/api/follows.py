from fastapi import APIRouter, Depends, HTTPException, status

from app.api.auth import getCurrentUser
from app.schemas.follow import FollowListResponse
from app.services.follow_service import followUser, listFollowers, listFollowing, listFriends, unfollowUser


router = APIRouter(prefix="/follows", tags=["follows"])


@router.post("/{user_id}")
def follow(
    user_id: int,
    currentUser: dict[str, str | int | None] = Depends(getCurrentUser),
) -> dict[str, str]:
    isFollowed = followUser(int(currentUser["id"]), user_id)
    if not isFollowed:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot follow this user")

    return {"status": "ok"}


@router.delete("/{user_id}")
def unfollow(
    user_id: int,
    currentUser: dict[str, str | int | None] = Depends(getCurrentUser),
) -> dict[str, str]:
    isUnfollowed = unfollowUser(int(currentUser["id"]), user_id)
    if not isUnfollowed:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot unfollow this user")

    return {"status": "ok"}


@router.get("/following", response_model=FollowListResponse)
def getFollowing(currentUser: dict[str, str | int | None] = Depends(getCurrentUser)) -> FollowListResponse:
    return FollowListResponse(items=listFollowing(int(currentUser["id"])))


@router.get("/followers", response_model=FollowListResponse)
def getFollowers(currentUser: dict[str, str | int | None] = Depends(getCurrentUser)) -> FollowListResponse:
    return FollowListResponse(items=listFollowers(int(currentUser["id"])))


@router.get("/friends", response_model=FollowListResponse)
def getFriends(currentUser: dict[str, str | int | None] = Depends(getCurrentUser)) -> FollowListResponse:
    return FollowListResponse(items=listFriends(int(currentUser["id"])))
