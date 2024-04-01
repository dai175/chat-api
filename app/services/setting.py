from typing import cast
from uuid import UUID

from sqlalchemy.orm import Session

from app.domains.setting import SettingDomain
from app.models import User
from app.schemas.request.setting import PostSettingParams
from app.schemas.response.setting import PostSettingRes


class SettingService:
    def __init__(self, db: Session, user: User) -> None:
        self.__db = db
        self.__user = user

    def update_setting(self, params: PostSettingParams) -> PostSettingRes:
        notification_setting = SettingDomain(db=self.__db, user=self.__user).update_setting(params=params)
        response = PostSettingRes(
            id=cast(UUID, notification_setting.id),
            notification_method=notification_setting.method,
        )
        return response
