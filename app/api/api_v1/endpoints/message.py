from uuid import UUID

from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_user_from_token
from app.db.db import get_db
from app.models import User
from app.schemas.request.message import PostMessageParams
from app.schemas.response.message import GetMessageRes, GetMessagesRes, PostMessageRes
from app.services.message import MessageService

router = APIRouter()


@router.get(
    "/messages",
    response_model=GetMessagesRes,
    name="メッセージ一覧取得",
)
async def get_messages(
    user: User = Depends(get_user_from_token),
    db: Session = Depends(get_db),
) -> GetMessagesRes:
    messages = MessageService(db=db, user=user).get_messages()
    return messages


@router.get(
    "/messages/{message_id}",
    response_model=GetMessageRes,
    name="メッセージ取得",
)
async def get_message(
    message_id: UUID,
    user: User = Depends(get_user_from_token),
    db: Session = Depends(get_db),
) -> GetMessageRes:
    message = MessageService(db=db, user=user).get_message(message_id=message_id)
    return message


@router.post("/messages", response_model=PostMessageRes, name="メッセージ作成", status_code=status.HTTP_201_CREATED)
async def post_message(
    request: Request,
    params: PostMessageParams,
    user: User = Depends(get_user_from_token),
    db: Session = Depends(get_db),
) -> PostMessageRes:
    message = await MessageService(db=db, user=user, request=request).create_message(params=params)
    return message


@router.delete("/messages/{message_id}", name="メッセージ削除", status_code=status.HTTP_204_NO_CONTENT)
async def delete_messages(
    message_id: UUID,
    user: User = Depends(get_user_from_token),
    db: Session = Depends(get_db),
) -> None:
    MessageService(db=db, user=user).delete_message(message_id=message_id)


@router.put("/messages/{message_id}/read", name="メッセージ既読", status_code=status.HTTP_204_NO_CONTENT)
async def put_messages_read(
    message_id: UUID,
    user: User = Depends(get_user_from_token),
    db: Session = Depends(get_db),
) -> None:
    MessageService(db=db, user=user).set_message_as_read(message_id=message_id)
