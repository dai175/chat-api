from typing import cast
from uuid import UUID

from sqlalchemy.orm import Session

from app.crud import crud_notification_setting
from app.models import NotificationSetting, User
from app.schemas.request.setting import PostSettingParams


class SettingDomain:
    def __init__(self, db: Session, user: User) -> None:
        self.__db = db
        self.__user = user

    def update_setting(self, params: PostSettingParams) -> NotificationSetting:
        notification_setting = crud_notification_setting.get_by_user_id(
            db=self.__db, user_id=cast(UUID, self.__user.id)
        )
        if not notification_setting:
            notification_setting = NotificationSetting(user_id=self.__user.id)
        notification_setting.method = params.notification_method
        updated_notification_setting = crud_notification_setting.create_or_update(
            db=self.__db, model=notification_setting
        )
        return updated_notification_setting
