from typing import cast
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.env import PUSHER_INSTANCE_ID
from app.core.messages import ErrorMessages
from app.crud import crud_user
from app.db.db import get_db
from app.services.user import UserService
from app.views.templates_config import templates

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login", response_class=HTMLResponse)
async def login(
    request: Request,
    form: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    token = UserService(db=db).login(form=form)
    user = crud_user.get_by_email(db=db, email=form.username)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=ErrorMessages.LOGIN_FAILED)
    return templates.TemplateResponse(
        "chat.html",
        {
            "request": request,
            "user_id": str(cast(UUID, user.id)),
            "access_token": token.access_token,
            "instance_id": PUSHER_INSTANCE_ID,
        },
    )
