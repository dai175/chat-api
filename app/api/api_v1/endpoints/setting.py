from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_user_from_token
from app.db.db import get_db
from app.models import User
from app.schemas.request.setting import PostSettingParams
from app.schemas.response.setting import PostSettingRes
from app.services.setting import SettingService

router = APIRouter()


@router.post(
    "/settings/notifications",
    response_model=PostSettingRes,
    name="通知設定登録",
)
async def post_notification_setting(
    params: PostSettingParams,
    user: User = Depends(get_user_from_token),
    db: Session = Depends(get_db),
) -> PostSettingRes:
    setting = SettingService(db=db, user=user).update_setting(params=params)
    return setting
