import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from starlette import status

from app.core.auth import decode_token_and_get_user
from app.core.messages import ErrorMessages
from app.db.db import get_db
from app.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_user_from_token(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    try:
        user = decode_token_and_get_user(db=db, token=token)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=ErrorMessages.INVALID_TOKEN,
            )
        return user
    except jwt.DecodeError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ErrorMessages.INVALID_TOKEN,
            headers={"WWW-Authenticate": "Bearer"},
        )
