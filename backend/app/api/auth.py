from fastapi import APIRouter, Depends, Header, HTTPException, status

from app.core.security import createAccessToken, decodeAccessToken
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse, UserResponse
from app.services.user_service import authenticateUser, createUser, formatUser, getUserById


router = APIRouter(prefix="/auth", tags=["auth"])


def getCurrentUser(authorization: str | None = Header(default=None)) -> dict[str, str | int | None]:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing token")

    token = authorization.split(" ", 1)[1]
    payload = decodeAccessToken(token)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    userId = payload.get("sub")
    if not isinstance(userId, str) or not userId.isdigit():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token subject")

    row = getUserById(int(userId))
    if row is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    return formatUser(row)


def getOptionalCurrentUser(authorization: str | None = Header(default=None)) -> dict[str, str | int | None] | None:
    if not authorization:
        return None

    return getCurrentUser(authorization)


def isSupervisor(user: dict[str, str | int | None]) -> bool:
    return user.get("id") == 0 and user.get("username") == "NBest" and user.get("role") == "admin"


def getCurrentAdmin(
    currentUser: dict[str, str | int | None] = Depends(getCurrentUser),
) -> dict[str, str | int | None]:
    if currentUser.get("role") != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")

    return currentUser


def getCurrentSupervisor(
    currentUser: dict[str, str | int | None] = Depends(getCurrentAdmin),
) -> dict[str, str | int | None]:
    if not isSupervisor(currentUser):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Supervisor access required")

    return currentUser


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register(request: RegisterRequest) -> TokenResponse:
    if request.password != request.confirm_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Passwords do not match")

    nickname = request.nickname or request.username
    user = createUser(request.username, request.password, nickname)
    if user is None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exists")

    token = createAccessToken(subject=str(user["id"]), role=str(user["role"]))
    return TokenResponse(access_token=token, user=UserResponse(**user))


@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest) -> TokenResponse:
    user = authenticateUser(request.username, request.password)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")

    token = createAccessToken(subject=str(user["id"]), role=str(user["role"]))
    return TokenResponse(access_token=token, user=UserResponse(**user))


@router.get("/me", response_model=UserResponse)
def getMe(currentUser: dict[str, str | int | None] = Depends(getCurrentUser)) -> UserResponse:
    return UserResponse(**currentUser)
