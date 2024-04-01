from typing import cast
from uuid import UUID

from fastapi import WebSocket
from sqlalchemy.orm import Session

from app.models import User
from app.schemas.request.message import PostMessageParams
from app.services.message import MessageService
from app.websocket.direct_chat_manager import direct_chat_manager


class DirectChatService:
    def __init__(self, db: Session, user: User, websocket: WebSocket, receiver_id: UUID):
        self.__websocket = websocket
        self.__receiver_id = receiver_id
        self.__user = user
        self.__message_service = MessageService(db=db, user=user)

    async def handle_connection(self):
        await direct_chat_manager.connect(
            websocket=self.__websocket, user_id=cast(UUID, self.__user.id), receiver_id=self.__receiver_id
        )

    async def handle_message(self):
        while True:
            content = await self.__websocket.receive_text()
            is_receiver_active = await direct_chat_manager.is_active_user(user_id=self.__receiver_id)
            if is_receiver_active:
                await direct_chat_manager.send_message(
                    message=f"{self.__user.email} says: {content}",
                    receiver_id=self.__receiver_id,
                    sender_id=cast(UUID, self.__user.id),
                )
            await self.send_message(content=content, is_receiver_active=is_receiver_active)

    async def send_message(self, content: str, is_receiver_active: bool):
        param = PostMessageParams(content=content, receiver_ids=[self.__receiver_id], is_read=is_receiver_active)
        await self.__message_service.create_message(params=param)

    async def handle_disconnection(self):
        direct_chat_manager.disconnect(user_id=cast(UUID, self.__user.id), receiver_id=self.__receiver_id)
        await direct_chat_manager.send_message(
            message=f"{self.__user.email} left the room", receiver_id=self.__receiver_id
        )
