from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db.db import get_db
from app.schemas.request.user import RegisterParams
from app.schemas.response.user import RegisterRes, TokenRes
from app.services.user import UserService

router = APIRouter()


@router.post("/register", response_model=RegisterRes)
async def register(
    params: RegisterParams,
    db: Session = Depends(get_db),
) -> RegisterRes:
    user = UserService(db=db).register(params=params)
    return user


@router.post("/token", response_model=TokenRes)
async def login(
    form: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
) -> TokenRes:
    response = UserService(db=db).login(form=form)
    return response
