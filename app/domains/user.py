from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.core.env import CRYPT_SCHEME
from app.core.messages import ErrorMessages
from app.crud import crud_user
from app.models import User
from app.schemas.request.user import RegisterParams


class UserDomain:
    def __init__(self, db: Session) -> None:
        self.__db = db
        self.__pwd_context = CryptContext(schemes=[CRYPT_SCHEME], deprecated="auto")

    def register(self, params: RegisterParams) -> User:
        user = User(
            email=params.email,
            hashed_password=self.__pwd_context.hash(params.password),
        )
        created_user = crud_user.create_or_update(db=self.__db, model=user)
        return created_user

    def login(self, form: OAuth2PasswordRequestForm) -> User:
        user = crud_user.get_by_email(db=self.__db, email=form.username)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=ErrorMessages.LOGIN_FAILED)
        if not self.__pwd_context.verify(form.password, user.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=ErrorMessages.LOGIN_FAILED)
        return user
