import jwt
from fastapi import Depends, Query, WebSocketException
from sqlalchemy.orm import Session
from starlette import status

from app.core.auth import decode_token_and_get_user
from app.db.db import get_db
from app.models import User


def get_user_from_token(
    token: str | None = Query(None),
    db: Session = Depends(get_db),
) -> User:
    try:
        if not token:
            raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)

        user = decode_token_and_get_user(db=db, token=token)
        if not user:
            raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)

        return user
    except jwt.DecodeError:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
