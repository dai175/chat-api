from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.messages import ErrorMessages
from app.models import NotificationSetting


def get_by_user_id(db: Session, user_id: UUID) -> NotificationSetting | None:
    return (
        db.query(NotificationSetting)
        .filter(
            NotificationSetting.user_id == user_id,
            NotificationSetting.deleted_at.is_(None),
        )
        .one_or_none()
    )


def create_or_update(db: Session, model: NotificationSetting) -> NotificationSetting:
    try:
        db.add(model)
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=ErrorMessages.MODEL_SAVE_FAILED)
    return model
