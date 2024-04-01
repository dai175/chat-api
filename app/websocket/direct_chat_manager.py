from uuid import UUID

from fastapi import WebSocket


class DirectChatManager:
    def __init__(self):
        self.__active_connections: dict[UUID, WebSocket] = {}
        self.__receivers: dict[UUID, UUID] = {}

    async def connect(self, websocket: WebSocket, user_id: UUID, receiver_id: UUID):
        await websocket.accept()
        self.__active_connections[user_id] = websocket
        self.__receivers[user_id] = receiver_id

    def disconnect(self, user_id: UUID, receiver_id: UUID):
        self.__active_connections.pop(user_id)
        if self.__receivers.get(user_id) == receiver_id:
            del self.__receivers[user_id]

    async def send_message(self, message: str, receiver_id: UUID, sender_id: UUID | None = None):
        if not sender_id or self.__receivers.get(sender_id) == receiver_id:
            await self.__active_connections[receiver_id].send_text(message)

    async def is_active_user(self, user_id: UUID) -> bool:
        return user_id in self.__active_connections


direct_chat_manager = DirectChatManager()
