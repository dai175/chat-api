from fastapi import APIRouter

from app.views.endpoints import login

router = APIRouter()

router.include_router(login.router, tags=["views"])
