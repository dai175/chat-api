from uuid import UUID

from fastapi import WebSocket


class GroupChatManager:
    def __init__(self):
        self.__active_connections: dict[UUID, WebSocket] = {}
        self.__rooms: dict[str, list[UUID]] = {}

    async def connect(self, websocket: WebSocket, user_id: UUID, room_id: str):
        await websocket.accept()
        self.__active_connections[user_id] = websocket
        if room_id in self.__rooms:
            self.__rooms[room_id].append(user_id)
        else:
            self.__rooms[room_id] = [user_id]

    def disconnect(self, user_id: UUID, room_id: str):
        self.__active_connections.pop(user_id)
        self.__rooms[room_id].remove(user_id)

    async def send_message(self, message: str, room_id: str):
        for user_id in self.__rooms[room_id]:
            await self.__active_connections[user_id].send_text(message)

    def get_user_ids_in_room(self, room_id: str) -> list[UUID]:
        return self.__rooms[room_id]


group_chat_manager = GroupChatManager()
