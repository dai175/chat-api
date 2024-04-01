from fastapi import APIRouter

from app.api.api_v1.endpoints import message, setting, user

router = APIRouter()

router.include_router(user.router, tags=["users"])
router.include_router(message.router, prefix="/api/v1", tags=["messages"])
router.include_router(setting.router, prefix="/api/v1", tags=["settings"])
