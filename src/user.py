import datetime
import logging
from typing import Optional
import jwt

from fastapi import Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.config import settings
from src.models import User
from fastapi import HTTPException

_logger = logging.getLogger(__name__)
security = HTTPBearer(auto_error=False)
DEFAULT_TOKEN = ["xxx", "undefined"]


def get_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> Optional[User]:
    try:
        if credentials is None:
            return None
        jwt_token = credentials.credentials
        if not jwt_token or jwt_token in DEFAULT_TOKEN:
            return None
        payload = jwt.decode(
            jwt_token, settings.jwt_secret, algorithms=["HS256"])
        jwt_payload = User.model_validate(payload)
        if jwt_payload.expire_at < datetime.datetime.now().timestamp():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Token 已过期，请重新登录")
        return jwt_payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token 已过期，请重新登录")
    except jwt.InvalidTokenError:
        _logger.warning("Invalid JWT token")
        return None
    except HTTPException:
        raise
    except Exception as e:
        _logger.error(f"Unexpected error in get_user: {e}")
        return None
