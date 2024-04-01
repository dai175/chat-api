from typing import cast
from uuid import UUID

from fastapi import WebSocket
from sqlalchemy.orm import Session

from app.models import User
from app.schemas.request.message import PostMessageParams
from app.services.message import MessageService
from app.websocket.group_chat_manager import group_chat_manager


class GroupChatService:
    def __init__(self, db: Session, user: User, websocket: WebSocket, room_id: str):
        self.__websocket = websocket
        self.__room_id = room_id
        self.__user = user
        self.__message_service = MessageService(db=db, user=user)

    async def handle_connection(self):
        await group_chat_manager.connect(
            websocket=self.__websocket, user_id=cast(UUID, self.__user.id), room_id=self.__room_id
        )

    async def handle_message(self):
        while True:
            content = await self.__websocket.receive_text()
            await group_chat_manager.send_message(
                message=f"{self.__user.email} says: {content}", room_id=self.__room_id
            )
            await self.send_message(content)

    async def send_message(self, content: str):
        user_ids = group_chat_manager.get_user_ids_in_room(room_id=self.__room_id)
        param = PostMessageParams(content=content, receiver_ids=user_ids, is_read=True)
        await self.__message_service.create_message(params=param)

    async def handle_disconnection(self):
        group_chat_manager.disconnect(user_id=cast(UUID, self.__user.id), room_id=self.__room_id)
        await group_chat_manager.send_message(message=f"{self.__user.email} left the room", room_id=self.__room_id)
