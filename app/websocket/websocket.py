from fastapi import APIRouter

from app.websocket.endpoints import chat

router = APIRouter()

router.include_router(chat.router, tags=["chats"])
