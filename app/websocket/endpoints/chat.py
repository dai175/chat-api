from uuid import UUID

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session

from app.core.messages import WebsocketErrorMessages
from app.crud import crud_user
from app.db.db import get_db
from app.models import User
from app.services.direct_chat import DirectChatService
from app.services.group_chat import GroupChatService
from app.websocket.dependencies import get_user_from_token

router = APIRouter()


@router.websocket("/group-chat/{room_id}")
async def group_chat(
    *,
    websocket: WebSocket,
    room_id: str,
    user: User = Depends(get_user_from_token),
    db: Session = Depends(get_db),
):
    chat_service = GroupChatService(db=db, user=user, websocket=websocket, room_id=room_id)
    await chat_service.handle_connection()
    try:
        await chat_service.handle_message()
    except WebSocketDisconnect:
        await chat_service.handle_disconnection()


@router.websocket("/direct-chat/{receiver_id_str}")
async def direct_chat(
    *,
    websocket: WebSocket,
    receiver_id_str: str,
    user: User = Depends(get_user_from_token),
    db: Session = Depends(get_db),
):
    receiver_id = await verify_receiver(db=db, receiver_id_str=receiver_id_str)
    if receiver_id is None:
        await websocket.close(
            code=WebsocketErrorMessages.INVALID_RECEIVER.code,
            reason=WebsocketErrorMessages.INVALID_RECEIVER.reason,
        )
        return

    chat_service = DirectChatService(db=db, user=user, websocket=websocket, receiver_id=receiver_id)
    await chat_service.handle_connection()
    try:
        while True:
            await chat_service.handle_message()
    except WebSocketDisconnect:
        await chat_service.handle_disconnection()


async def verify_receiver(db: Session, receiver_id_str: str) -> UUID | None:
    try:
        receiver_id = UUID(receiver_id_str)
    except ValueError:
        return None

    receiver = crud_user.get_by_id(db=db, user_id=receiver_id)
    if not receiver:
        return None

    return receiver_id
