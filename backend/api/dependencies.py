import os
from typing import Optional

from fastapi import Header, HTTPException, status


def require_api_key(x_api_key: Optional[str] = Header(default=None)) -> None:
    """API 키 인증을 수행한다."""
    expected = os.getenv("API_KEY")
    if not expected:
        return
    if x_api_key != expected:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )
