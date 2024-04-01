from datetime import datetime, timedelta, timezone
from typing import cast
from uuid import UUID

import jwt
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.env import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY, TOKEN_TYPE
from app.domains.user import UserDomain
from app.schemas.request.user import RegisterParams
from app.schemas.response.user import RegisterRes, TokenRes


class UserService:
    def __init__(self, db: Session) -> None:
        self.__db = db

    def register(self, params: RegisterParams) -> RegisterRes:
        created_user = UserDomain(db=self.__db).register(params=params)
        response = RegisterRes(
            id=cast(UUID, created_user.id),
            email=created_user.email,
            created_at=created_user.created_at,
            updated_at=created_user.updated_at,
        )
        return response

    def login(self, form: OAuth2PasswordRequestForm) -> TokenRes:
        user = UserDomain(db=self.__db).login(form=form)
        token = self.create_access_token(
            data={"sub": user.email},
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        )
        response = TokenRes(access_token=token, token_type=TOKEN_TYPE)
        return response

    @staticmethod
    def create_access_token(data: dict[str, str], expires_delta: timedelta) -> str:
        expire = datetime.now(timezone.utc) + expires_delta
        return jwt.encode({**data, "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)
