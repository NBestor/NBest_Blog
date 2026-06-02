import base64
import hashlib
import hmac
import json
import secrets
from datetime import datetime, timedelta, timezone

from app.core.config import getSettings


def _encodeBase64Url(value: bytes) -> str:
    return base64.urlsafe_b64encode(value).rstrip(b"=").decode("utf-8")


def _decodeBase64Url(value: str) -> bytes:
    padding = "=" * (-len(value) % 4)
    return base64.urlsafe_b64decode(value + padding)


def getPasswordHash(password: str) -> str:
    salt = secrets.token_hex(16)
    passwordHash = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), 120000)
    return f"pbkdf2_sha256${salt}${passwordHash.hex()}"


def verifyPassword(password: str, passwordHash: str) -> bool:
    try:
        algorithm, salt, expectedHash = passwordHash.split("$")
    except ValueError:
        return False

    if algorithm != "pbkdf2_sha256":
        return False

    currentHash = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), 120000)
    return hmac.compare_digest(currentHash.hex(), expectedHash)


def createAccessToken(subject: str, role: str) -> str:
    settings = getSettings()
    expireTime = datetime.now(timezone.utc) + timedelta(minutes=settings.jwt_expire_minutes)
    header = {"alg": "HS256", "typ": "JWT"}
    payload = {"sub": subject, "role": role, "exp": int(expireTime.timestamp())}

    encodedHeader = _encodeBase64Url(json.dumps(header, separators=(",", ":")).encode("utf-8"))
    encodedPayload = _encodeBase64Url(json.dumps(payload, separators=(",", ":")).encode("utf-8"))
    signingInput = f"{encodedHeader}.{encodedPayload}".encode("utf-8")
    signature = hmac.new(settings.jwt_secret_key.encode("utf-8"), signingInput, hashlib.sha256).digest()

    return f"{encodedHeader}.{encodedPayload}.{_encodeBase64Url(signature)}"


def decodeAccessToken(token: str) -> dict[str, str | int] | None:
    settings = getSettings()

    try:
        encodedHeader, encodedPayload, encodedSignature = token.split(".")
    except ValueError:
        return None

    signingInput = f"{encodedHeader}.{encodedPayload}".encode("utf-8")
    expectedSignature = hmac.new(settings.jwt_secret_key.encode("utf-8"), signingInput, hashlib.sha256).digest()

    if not hmac.compare_digest(_encodeBase64Url(expectedSignature), encodedSignature):
        return None

    try:
        payload = json.loads(_decodeBase64Url(encodedPayload))
    except (json.JSONDecodeError, ValueError):
        return None

    expireTimestamp = payload.get("exp")
    if not isinstance(expireTimestamp, int) or expireTimestamp < int(datetime.now(timezone.utc).timestamp()):
        return None

    return payload
